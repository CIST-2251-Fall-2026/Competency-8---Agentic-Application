import requests
import json
from pathlib import Path

INDICATORS = {
    "SP.POP.TOTL": "Total population",
    "NY.GDP.MKTP.CD": "GDP in current US dollars",
    "NY.GDP.PCAP.CD": "GDP per capita",
    "SP.DYN.LE00.IN": "Life expectancy",
    "EN.ATM.CO2E.PC": "CO2 emissions per person"
}

SOURCE = "World Bank Indicators API"


def find_indicator(query):
    return {
        code: name for code, name in INDICATORS.items()
        if query.lower() in name.lower()
        or query.upper() == code
    }


def get_data(country, indicator, year, offline=False):
    country = country.upper()

    if indicator not in INDICATORS:
        return {"error": "Unknown indicator"}

    if len(country) != 3 or not country.isalpha():
        return {"error": "Invalid country code"}

    if not isinstance(year, int) or not 1960 <= year <= 2026:
        return {"error": "Invalid year"}

    url = (
        f"https://api.worldbank.org/v2/country/"
        f"{country}/indicator/{indicator}"
    )

    try:
        if offline:
            raise requests.ConnectionError("Offline mode")

        response = requests.get(
            url,
            params={"format": "json", "date": year},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if len(data) < 2 or not data[1]:
            return {"error": "No observations found"}

        value = data[1][0]["value"]
        source = SOURCE

    except (requests.RequestException, ValueError):
        path = Path(__file__).with_name("fallback.json")

        try:
            backup = json.loads(path.read_text())
            key = f"{country}:{indicator}:{year}"

            if key not in backup:
                return {"error": "API and backup data unavailable"}

            value = backup[key]
            source = SOURCE + " (local fallback)"

        except (OSError, ValueError):
            return {"error": "Backup unavailable"}

    if value is None:
        return {"error": "Missing observation"}

    return {
        "country": country,
        "indicator": INDICATORS[indicator],
        "year": year,
        "value": value,
        "source": source
    }


def compare_values(first, second):
    return {
        "first": first,
        "second": second,
        "difference": second - first
    }


def calculate_change(old, new):
    return {
        "change": new - old,
        "percent_change": (
            round((new - old) / old * 100, 2)
            if old != 0 else None
        )
    }