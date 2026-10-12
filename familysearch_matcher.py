import csv
import io
import json
import re
import requests


def clean_text(text: str) -> str:
    """
    Normalizes input text by converting to uppercase, removing special 
    characters/punctuation, and stripping redundant whitespace.
    """
    if not text or not isinstance(text, str):
        return ""
    
    cleaned = text.upper()
    cleaned = re.sub(r"[^A-Z\s]", "", cleaned)
    cleaned = " ".join(cleaned.split())
    return cleaned


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculates similarity score (0.0 to 1.0) using bigram token overlap
    between two cleaned strings for accurate fuzzy matching.
    """
    s1 = clean_text(str1)
    s2 = clean_text(str2)

    if not s1 or not s2:
        return 0.0
    if s1 == s2:
        return 1.0

    # Generate character bigrams for token-based fuzzy matching
    b1 = set(s1[i:i+2] for i in range(len(s1) - 1))
    b2 = set(s2[i:i+2] for i in range(len(s2) - 1))

    if not b1 or not b2:
        return 0.0

    intersection = b1.intersection(b2)
    union = b1.union(b2)

    return round(len(intersection) / len(union), 2)


def fetch_census_records(source_url: str, fallback_file: str = "fallback_data.json") -> list:
    """
    Fetches census records from a remote URL.
    Seamlessly falls back to local JSON file if network call fails or times out.
    """
    try:
        response = requests.get(source_url, timeout=5)
        response.raise_for_status()

        if "json" in response.headers.get("Content-Type", ""):
            records = response.json()
        else:
            csv_data = io.StringIO(response.text)
            reader = csv.DictReader(csv_data)
            records = [row for row in reader]

        print(" Successfully fetched live census records from remote endpoint.")
        return records

    except (requests.RequestException, Exception) as err:
        print(f"⚠️ Remote fetch failed ({err}). Activating local JSON fallback...")
        try:
            with open(fallback_file, "rt", encoding="utf-8") as infile:
                records = json.load(infile)
            return records
        except Exception as file_err:
            print(f" Error loading fallback file: {file_err}")
            return []


def find_duplicates(records: list, threshold: float = 0.60) -> list:
    """
    Iterates through census records and identifies potential duplicate pairs 
    based on fuzzy name similarity and birth year matching.
    """
    duplicates = []
    num_records = len(records)

    for i in range(num_records):
        for j in range(i + 1, num_records):
            r1 = records[i]
            r2 = records[j]

            name1 = f"{r1.get('first_name', '')} {r1.get('last_name', '')}"
            name2 = f"{r2.get('first_name', '')} {r2.get('last_name', '')}"
            score = calculate_similarity(name1, name2)

            b1 = r1.get("birth_year")
            b2 = r2.get("birth_year")
            year_match = True
            if b1 and b2:
                year_match = abs(int(b1) - int(b2)) <= 1

            if score >= threshold and year_match:
                duplicates.append({
                    "record1": r1.get("id"),
                    "name1": name1,
                    "record2": r2.get("id"),
                    "name2": name2,
                    "similarity_score": score
                })

    return duplicates


def main():
    """Main execution block."""
    print("=== FamilySearch & RLL Record Linker ===")
    
    rll_data_url = "https://raw.githubusercontent.com/byu-rll/sample-data/main/census.csv"
    
    records = fetch_census_records(rll_data_url)
    print(f"Total records loaded: {len(records)}")

    results = find_duplicates(records, threshold=0.60)
    
    print(f"\nPotential Duplicates Identified: {len(results)}")
    for match in results:
        print(f" Match [{int(match['similarity_score'] * 100)}%]: "
              f"{match['record1']} ({match['name1']}) <-> {match['record2']} ({match['name2']})")


if __name__ == "__main__":
    main()