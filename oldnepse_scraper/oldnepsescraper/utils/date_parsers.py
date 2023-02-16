import datetime as dt


def oldnepalstock_to_default(oldnepse_date: str) -> str:
    """
    Returns 'As of yyyy-mm-dd HH:MM:SS' by parsing into 'dd month, yyyy HH:MMam/pm' format
    """
    return dt.datetime.strptime(oldnepse_date, "As of %Y-%m-%d %H:%M:%S").strftime(
        "%d %B, %Y %I:%M%p"
    )
