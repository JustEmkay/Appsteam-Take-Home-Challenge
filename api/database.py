import sqlite3
from pathlib import Path

PATH = "db/journalData.db"

conn = sqlite3.connect(PATH, check_same_thread=False)
conn.isolation_level = None
cursor = conn.cursor()
cursor.execute(" PRAGMA foreign_keys = ON ")


def create_table() -> bool:
    
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS users(
                uid TEXT    PRIMARY KEY,
                username TEXT   NOT NULL,
                password BLOB   NOT NULL,
                q TEXT NOT NULL,
                a TEXT  NOT NULL
            )''')
    except Exception as e:
        print("Error[usertable]",e)
        
    try:
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS journals(
                jid TEXT    PRIMARY KEY,
                uid TEXT    NOT NULL,
                journal TEXT    NOT NULL,
                created_date INTEGER    NOT NULL,
                updated_date INTEGER    DEFAULT None,
                FOREIGN KEY (uid)
                    REFERENCES users(uid) ON DELETE CASCADE
            )'''
        )
    except Exception as e:
        print("Error[journalTable]",e)
        
         
def insertUser(**registerInfo)-> bool:
    
    try:
        cursor.execute('''
                       INSERT INTO users(uid, username,
                       password, q, a) VALUES(?, ?, ?, ?, ?)
                       ''', (registerInfo['uid'], registerInfo['username'],
                             registerInfo['password'], registerInfo['q'],
                             registerInfo['a']))
        
        return True

    except Exception as e:
        print("Error[insertUser]:",e)
        
        
def insertJournal(**journalInfo)-> bool:
    
    try:
        cursor.execute('''
                       INSERT INTO journals(jid, uid, journal,
                       created_date) VALUES(?, ?, ?, ?)
                       ''', (journalInfo['jid'], journalInfo['uid'],
                             journalInfo['journal'],
                             journalInfo['created_date'],))
        
        return True
    
    except Exception as e:
        print("Error[insertJournal]:",e)

    
def getJournals(uid: str, limit: int= None)-> dict:
    
    try:
        if not limit:
            cursor.execute('''SELECT jid, journal, created_date,
                        updated_date FROM journals WHERE uid=?
                        ORDER BY created_date DESC''',
                        (uid,))
        else:
            cursor.execute('''SELECT jid, journal, created_date,
                        updated_date FROM journals WHERE uid=?
                        ORDER BY created_date DESC''',
                        (uid,))
        #result: list[tuple[jid, journal, created_Date, updated_date]]
        result= cursor.fetchall() 
        
        journals: dict= {}
        for _ in result:
            
            journals.update( {
                _[0]: {
                'journal': _[1],
                'created_date': _[2],
                'updated_date': _[3]                    
                    }
                } )
        
        return journals
        
    except Exception as e:
        print("Error[getJournal]:",e)
        

def selectedJournal(uid: str, jids: list)-> dict:
    
    print(list(jids))
    
    placeholder: str= ",".join('?' for _ in jids)
    print(placeholder)
    try:
        cursor.execute(f"""
                       SELECT journal, created_date FROM journals WHERE uid= ? AND jid IN ({ placeholder })
                       """,(uid,)+tuple(jids))
        result= cursor.fetchall()
        tempDict: dict= {}
        for indx, _ in enumerate(result):
            tempDict.update({ jids[indx] :{'journal':_[0], 'created_date': _[1]}})
        
        return tempDict
        
        
    except Exception as e:
        print("Error[selectedJournal]:",e)

    
def verifyUsers(username: str, uid: str= None)-> tuple:
    
    try:
        if not uid:
            cursor.execute(''' 
                        SELECT uid FROM users WHERE username= ? ''',
                        (username,))

        else:
            cursor.execute(''' 
                        SELECT uid, username, password FROM users WHERE username= ? AND uid= ?''',
                        (username, uid, ))            
        
        result= cursor.fetchone()
        print(result)
        return result
        
    except Exception as e:
        print("Error[readJournal]:",e)
    
    
def updateJournal( journal: str, journalID: str, userID: str )-> bool:
    
    try:
        
        cursor.execute(
            ''' UPDATE journals SET journal= ? WHERE jid= ? AND uid= ? ''',
            (journal, journalID, userID,)
        )
        
    except Exception as e:
        print("Error[updateJournal]:", e)
    
           
def deleteUser( userID: str )-> bool:
    
    try:
        cursor.execute(
            ''' DELETE FROM users WHERE uid= ?''',(userID,)
        )
                
    except Exception as e:
        print("Error[deleteUser]",e)


def deleteJournal( journalID: str )-> bool:
    
    try:
        cursor.execute(
            ''' DELETE FROM journal WHERE jid= ?''',(journalID,)
        )
                
    except Exception as e:
        print("Error[deleteUser]",e)


# getJournals(uid= "dadada")

# create_table()

# insertUser( uid="dadada", username='vasu',
#            password='123456', q='gf name', a='juhi' )

# insertJournal( uid='dadada', jid='dadada2',
#               journal='vasu loli', created_date= 123456789 )

# updateJournal(journal= 'lalu loli', userID='dadada', journalID='dadada2')

# deleteUser('dadada')

# print(verifyUser(username="vasu", password='123456'))