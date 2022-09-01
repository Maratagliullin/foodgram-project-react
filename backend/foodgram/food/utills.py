def search_in_result_data(value, dicts):
    """Служеюная функция поиска"""

    for key, item in enumerate(dicts):
        if item['title'] == value:
            return key
    return None
