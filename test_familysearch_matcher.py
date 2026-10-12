from familysearch_matcher import clean_text, calculate_similarity, find_duplicates


def test_clean_text():
    """Verify string normalization and punctuation removal."""
    assert clean_text("  john  smith!! ") == "JOHN SMITH"
    assert clean_text("MARCELA, JR.") == "MARCELA JR"


def test_calculate_similarity():
    """Verify similarity ratio logic across identical and distinct strings."""
    assert calculate_similarity("JOHN SMITH", "JOHN SMITH") == 1.0
    assert calculate_similarity("JOHN", "ALICE") == 0.0


def test_find_duplicates():
    """Verify duplicate identification on a controlled record dataset."""
    sample_records = [
        {"id": "1", "first_name": "John", "last_name": "Smith", "birth_year": 1880},
        {"id": "2", "first_name": "Jon", "last_name": "Smith", "birth_year": 1880},
        {"id": "3", "first_name": "Alice", "last_name": "Walker", "birth_year": 1900}
    ]
    matches = find_duplicates(sample_records, threshold=0.60)
    
    assert len(matches) == 1
    assert matches[0]["record1"] == "1" and matches[0]["record2"] == "2"