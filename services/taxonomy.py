import time
import requests
from config import Config


class SkillTaxonomy:
    def __init__(self):
        self._skills: list[dict] = []  # [{code, name, aliases}, ...]
        self._lookup: dict[str, str] = {}  # {normalized_term: code}
        self._last_fetched: float = 0

    def refresh_if_stale(self):
        now = time.time()
        if now - self._last_fetched > Config.TAXONOMY_REFRESH_SECONDS or not self._skills:
            self._fetch()

    def _fetch(self):
        url = f"{Config.BE_BASE_URL}/internal/skills"
        headers = {"Authorization": f"Bearer {Config.SERVICE_TOKEN}"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            payload = response.json()
            skills = payload.get("data", {}).get("skills", [])

            self._skills = skills
            self._build_lookup()
            self._last_fetched = time.time()
        except requests.RequestException as e:
            # Kalau BE tidak bisa dihubungi, tetap pakai cache lama (kalau ada)
            # supaya /extract-skills tidak total mati hanya karena refresh gagal.
            print(f"[taxonomy] gagal fetch dari BE: {e}")

    def _build_lookup(self):
        """
        Bangun dict pencarian: setiap nama & alias (lowercase) -> code.
        Nama/alias yang mengandung lebih dari 1 kata tetap disimpan utuh
        (matching multi-kata ditangani di matcher.py lewat substring check,
        bukan per-token, supaya "Machine Learning" tidak match parsial ke
        "Learning" doang).
        """
        lookup = {}
        for skill in self._skills:
            code = skill.get("code")
            if not code:
                continue

            terms = [skill.get("name", "")] + (skill.get("aliases") or [])
            for term in terms:
                if term:
                    lookup[term.strip().lower()] = code

        self._lookup = lookup

    def get_lookup(self) -> dict[str, str]:
        self.refresh_if_stale()
        return self._lookup

    def get_all_terms_sorted_by_length(self) -> list[tuple[str, str]]:
        """
        Return list (term, code) diurutkan dari term terpanjang ke terpendek.
        Penting supaya "machine learning" dicek duluan sebelum "learning"
        (mencegah partial match yang salah).
        """
        lookup = self.get_lookup()
        return sorted(lookup.items(), key=lambda x: len(x[0]), reverse=True)


# Singleton instance, dipakai bareng oleh seluruh aplikasi Flask.
taxonomy = SkillTaxonomy()