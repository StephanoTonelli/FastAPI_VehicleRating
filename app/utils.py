import pandas as pd

def load_scoring_rules_from_excel(file_path: str) -> dict:
    """
    Load scoring rules from an Excel file and return them as a dictionary.
    """
    df = pd.read_excel(file_path)
    rules = {}
    for _, row in df.iterrows():
        rules[row['category']] = {
            'weight': row['weight'],
            'condition': row['condition']  # e.g., "engine_size > X"
        }
    return rules
