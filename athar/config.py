"""Athar program constants — the single place to change rates, quotas and prizes.

Every value here was confirmed by the program owner (Asmaa) in October 2026.
If you change one, change it in the two page templates too (search for FX / QUOTA in
templates/internal.html), because the internal page re-computes in the browser when a
file is uploaded there.
"""

# Fixed company FX rates to SAR. Sales and targets arrive in each country's own currency.
# NEVER add two currencies together; convert to SAR first.
FX = {"KSA": 1.0, "UAE": 1.02, "Oman": 9.75, "Kuwait": 12.30, "Bahrain": 10.0, "Qatar": 1.03}

# Country (from the target file) -> prize market
MARKET = {"KSA": "KSA", "UAE": "UAE", "Oman": "Oman", "Kuwait": "KW-BH", "Bahrain": "KW-BH", "Qatar": "Qatar"}

# Prize seats per market (40 in total, car excluded)
QUOTA = {"KSA": 34, "UAE": 2, "Oman": 2, "KW-BH": 2}
SMALL_MARKETS = ("UAE", "Oman", "KW-BH")      # 1st place = phone (B), 2nd place = gold bar (E)
PER_CATEGORY = 10                              # 10 phones, 10 iPads, 10 watches, 10 gold bars

# Car (A): company-wide race, minimum projected/actual sales in SAR
CAR_MIN_SAR = 300_000

PRIZE = {"A": "سيارة", "B": "جوال ذكي", "C": "آيباد", "D": "ساعة ذكية", "E": "سبيكة ذهب"}

# Branches that never take part (EXBUAE = temporary UAE exhibition, closed)
EXCLUDE = {"EXBUAE"}

# Live Odoo POS codes that drifted from the master's target codes mid-period (same physical branch,
# renamed account — usually a "2" suffix, or HA-MEDAD). Maps API store_name (UPPER) -> master target
# code so the branch's sales join instead of showing 0%. Add new drifts here (the build prints
# "WARNING branches with sales but no target" for any still unmatched).
API_ALIASES = {
    "ALAQUEQ2": "ALAQUEQ",          # Aqiq Street, Riyadh
    "HA-MEDAD": "MEDAD",            # Medad Center Match, Riyadh
    "ALWATANIAH2": "ALWATANIAH",   # Al Wataniyah, Hafer Al Batin
    "MILAGROPLZ2": "MILAGROPLZ",   # Milagro Plaza, Tabuk
    "ALHAZIM2": "ALHAZIM",         # Al Hizam, Abha
    "ABHATIMESQ2": "ABHATIMESQ",   # Time Square, Abha
    "HAKHAMBLV2": "HAKHAMBLV",     # Boulivard, Khamis Meshaet
    "HAHAILZONE2": "HAHAILZONE",   # Hail Zone, Hail
    "HAKHALELSQ": "KHALIL SUQARE", # Khalil Square, Makkah (matched by name)
}

# Personal employee POS accounts look like "1238-Abdellah", "6253 -WAlotibi" or "Aalzhrani-6563".
# Anything else (shared/branch accounts) is ignored when picking the branch's winner.
EMP_PATTERN = r"(^\d{3,}\s*-)|(-\s*\d{3,}$)"

# One employee with more than this share of the branch's sales -> flag for review
REVIEW_SHARE = 0.60
