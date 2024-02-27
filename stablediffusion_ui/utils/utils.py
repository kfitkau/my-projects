import json

def get_translations(language: str) -> dict:
    """
    Get translations for a specified language from a JSON file.

    Args:
        language (str): Language code used to construct the JSON file name.

    Returns:
        dict: Dictionary containing translations.
    """
    with open(f'./assets/json/i18n-{language}.json', encoding='utf-8') as f:
        data = json.load(f)
    return data

def load_scheduler_options_from_file(file_path: str) -> list:
    """
    Load scheduler options from a file.

    Args:
        file_path (str): Path to the file containing scheduler options.

    Returns:
        list: List of scheduler options.
    """
    with open(file_path, 'r') as file:
        options = [line.strip() for line in file]
    return options