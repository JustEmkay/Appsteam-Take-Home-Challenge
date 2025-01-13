import hashlib
import datetime


# fn: Convert timestamp to datetime[ dd/mm/yy, HH:MM:SS AM/PM ]
def timestamp2Datetime( timestamp: int)-> None:
    return datetime.datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y, %I:%M:%S %p")

# fn: Return dict based of filter option[ 'day', 'week', 'month', 'year', 'all' ]
def filterJournal( journalsData: dict, option: str ) -> dict:
    
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

def hashList( selectedList: list )-> str:
    
    l2s: str= "".join(selectedList)
    return hashlib.sha256(l2s.encode()).hexdigest()

