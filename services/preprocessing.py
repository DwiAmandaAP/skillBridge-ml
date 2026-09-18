import re


def clean_text(text: str) -> str:
    """
    Preprocessing teks lowongan: lowercase, hapus tanda baca berlebih,
    normalisasi spasi. Tidak menghapus karakter penting seperti '.' pada
    'Node.js' atau '#' pada 'C#' -- itu ditangani di level matching (matcher.py),
    bukan di sini, supaya nama skill dengan simbol tetap bisa dicocokkan.
    """
    if not text:
        return ""

    text = text.lower()

    # Hapus karakter yang jelas bukan bagian dari nama skill teknis
    # (tanda kurung, bullet point, dsb), tapi pertahankan . # + -
    text = re.sub(r"[•·▪●○◦‣⁃]", " ", text)
    text = re.sub(r"[\"'“”‘’]", " ", text)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def tokenize(text: str) -> list[str]:
    """
    Tokenisasi sederhana berbasis kata, mempertahankan simbol teknis
    (., #, +, -) di dalam token supaya 'node.js', 'c#', 'c++' tidak pecah.
    """
    cleaned = clean_text(text)
    tokens = re.findall(r"[a-z0-9][a-z0-9.#+_-]*", cleaned)
    return tokens