"""
Fallback skill dictionary: dipakai HANYA ketika exact/substring matching
terhadap taxonomy tidak menemukan skill apapun dari teks lowongan
(kasus umum: field 'skills' dari sumber data kosong).

Key: kata kunci yang dicari di title (lowercase, substring match sederhana).
Value: daftar skill CODE (harus match dengan kode yang ada di tabel `skills`
Laravel).

Urutan dictionary penting: dicek dari atas ke bawah, key PERTAMA yang cocok
dipakai. Taruh key yang lebih spesifik di atas key yang lebih umum.
"""

FALLBACK_RULES: list[tuple[str, list[str]]] = [
    # --- Web / Software Development ---
    ("full stack", [
        "javascript",
        "html_css",
        "css",
        "nodejs",
        "react",
        "mysql",
        "php",
        "laravel",
    ]),
    ("full-stack", [
        "javascript",
        "html_css",
        "nodejs",
        "react",
        "mysql",
        "php",
        "laravel",
    ]),
    ("fullstack", [
        "javascript",
        "html_css",
        "nodejs",
        "react",
        "mysql",
        "php",
        "laravel",
    ]),

    ("frontend", [
        "javascript",
        "html_css",
        "react",
        "vuejs",
    ]),
    ("front-end", [
        "javascript",
        "html_css",
        "react",
        "vuejs",
    ]),
    ("front end", [
        "javascript",
        "html_css",
        "react",
        "vuejs",
    ]),

    ("backend", [
        "php",
        "laravel",
        "mysql",
        "nodejs",
        "rest_api",
    ]),
    ("back-end", [
        "php",
        "laravel",
        "mysql",
        "nodejs",
        "rest_api",
    ]),
    ("back end", [
        "php",
        "laravel",
        "mysql",
        "nodejs",
        "rest_api",
    ]),

    ("web developer", [
        "mysql",
        "laravel",
        "javascript",
        "html_css",
        "php",
    ]),
    ("web development", [
        "mysql",
        "laravel",
        "javascript",
        "html_css",
        "php",
    ]),

    # --- Mobile ---
    ("android developer", [
        "kotlin",
        "java",
        "android_development",
    ]),
    ("ios developer", [
        "swift",
        "ios_development",
    ]),
    ("mobile developer", [
        "react_native",
        "flutter",
        "javascript",
    ]),
    ("flutter", [
        "flutter",
        "dart",
    ]),
    ("react native", [
        "react_native",
        "javascript",
    ]),

    # --- Data ---
    ("data engineer", [
        "sql",
        "python",
        "etl",
        "docker",
    ]),
    ("data analyst", [
        "sql",
        "excel",
        "powerbi",
    ]),
    ("data scientist", [
        "python",
        "machine_learning",
        "sql",
    ]),

    # --- AI / ML ---
    ("machine learning", [
        "python",
        "machine_learning",
    ]),
    ("ai engineer", [
        "python",
        "machine_learning",
        "artificial_intelligence",
    ]),
    ("computer vision", [
        "python",
        "computer_vision",
        "machine_learning",
    ]),
    ("nlp", [
        "python",
        "nlp",
    ]),

    # --- DevOps / Infra ---
    ("devops", [
        "docker",
        "kubernetes",
        "ci_cd",
    ]),
    ("cloud engineer", [
        "aws",
        "docker",
        "kubernetes",
    ]),
    ("system administrator", [
        "linux",
        "networking",
        "sysadmin",
    ]),
    ("sysadmin", [
        "linux",
        "networking",
        "sysadmin",
    ]),
    ("network engineer", [
        "networking",
        "tcp_ip",
    ]),

    # --- QA ---
    ("qa engineer", [
        "software_testing",
        "manual_testing",
        "automation_testing",
    ]),
    ("quality assurance", [
        "software_testing",
        "manual_testing",
        "automation_testing",
    ]),
    ("software tester", [
        "software_testing",
        "manual_testing",
    ]),

    # --- Security ---
    ("cyber security", [
        "cybersecurity",
        "network_security",
        "vulnerability_assessment",
    ]),
    ("cybersecurity", [
        "cybersecurity",
        "network_security",
        "vulnerability_assessment",
    ]),
    ("security engineer", [
        "network_security",
        "penetration_testing",
    ]),
    ("penetration test", [
        "penetration_testing",
    ]),
    ("pentest", [
        "penetration_testing",
    ]),

    # --- Design ---
    ("ui/ux", [
        "figma",
        "wireframing",
        "ui_design",
        "ux_design",
    ]),
    ("ui\\/ux", [
        "figma",
        "wireframing",
        "ui_design",
        "ux_design",
    ]),
    ("ux designer", [
        "figma",
        "wireframing",
        "ux_design",
    ]),
    ("ui designer", [
        "figma",
        "ui_design",
    ]),
    ("product designer", [
        "figma",
        "wireframing",
        "ui_design",
        "ux_design",
    ]),

    # --- Umum IT ---
    ("software engineer", [
        "javascript",
        "sql",
        "git",
    ]),
    ("programmer", [
        "javascript",
        "sql",
        "git",
    ]),
    ("it support", [
        "it_support",
        "problem_solving",
    ]),
]


def get_fallback_skills(title: str) -> list[str]:
    """
    Cari rule pertama yang key-nya muncul sebagai substring di title
    (lowercase). Return list skill code, atau [] kalau tidak ada yang cocok.
    """
    normalized_title = title.lower()

    for keyword, skill_codes in FALLBACK_RULES:
        if keyword in normalized_title:
            return skill_codes

    return []