import datetime


# fn: Convert timestamp to datetime[ dd/mm/yy, HH:MM:SS AM/PM ]
def timestamp2Datetime( timestamp: int)-> None:
    """
    Convert timestamp to datetime formatt of DD:MM:YYYY, HH:MM:SS AM/PM
    """
    return datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y, %I:%M:%S %p")

# fn: Return dict based of filter option[ 'day', 'week', 'month', 'year', 'all' ]
def filterJournal( journalsData: dict, option: str ) -> dict:
    """
    Filter journal entries based on a specified time period: 'day', 'week', 
    'month', 'year', or 'all'.

    Parameters
    ----------
    journalsData : dict
        A dictionary containing journal entries. Each key represents a unique 
        identifier, and its value is another dictionary with a `created_date` field 
        (timestamp).
    option : str
        The filter option to determine which entries to include. Options are:
        - 'Day': Filter by the current day.
        - 'Week': Filter by the current week.
        - 'Month': Filter by the current month.
        - 'Year': Filter by the current year.
        - 'All': Return all entries (default if option is not provided).

    Returns
    -------
    dict
        A dictionary containing filtered journal entries based on the selected 
        option. If no filter is applied or the option is 'All', returns the original 
        input dictionary.

    Examples
    --------
    >>> journalsData = {
    ...     "1": {"created_date": 1672531199, "content": "Journal entry 1"},
    ...     "2": {"created_date": 1672617599, "content": "Journal entry 2"}
    ... }
    >>> filterJournal(journalsData, "Day")
    {'1': {'created_date': 1672531199, 'content': 'Journal entry 1'}}

    >>> filterJournal(journalsData, "All")
    {'1': {'created_date': 1672531199, 'content': 'Journal entry 1'}, 
     '2': {'created_date': 1672617599, 'content': 'Journal entry 2'}}
    """


    optionsDict: dict= {
    "Day": datetime.datetime.now().day,
    "Week": datetime.datetime.now().isocalendar().week,
    "Month": datetime.datetime.now().month,
    "Year": datetime.datetime.now().year
    }

    if option == 'All' or not option:
        return journalsData

    options: list= list(optionsDict.keys())
    tempDict: dict= {}
    
    for key, data in journalsData.items():    
        if option == options[0]:
            if optionsDict[option] == datetime.datetime.fromtimestamp(data['created_date']).day:
                tempDict.update({key:data})
        elif option == options[1]:
            if optionsDict[option] == datetime.datetime.fromtimestamp(data['created_date']).isocalendar().week:
                tempDict.update({key:data})
        elif option == options[2]:
            if optionsDict[option] == datetime.datetime.fromtimestamp(data['created_date']).month:
                tempDict.update({key:data})
        elif option == options[3]:
            if optionsDict[option] == datetime.datetime.fromtimestamp(data['created_date']).year:
                tempDict.update({key:data})

    return tempDict            


