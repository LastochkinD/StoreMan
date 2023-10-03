from datetime import datetime

def str_to_date(date_string):
    try:
        date_object = datetime.strptime(date_string, "%d.%m.%Y").date()
        return date_object
    except ValueError:
        return None
