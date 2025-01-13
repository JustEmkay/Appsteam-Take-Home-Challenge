import requests


API_URL: str= 'http://127.0.0.1:8000'


def verifyUser( loginInfo ):
    req= requests.post(API_URL+ "/verify", json= dict(loginInfo))
    res= req.status_code
    if res== 200:
        return req.json()
    
def registerUser( userInfo ):
    req= requests.post(API_URL+ "/register", json= dict(userInfo))
    res= req.status_code
    if res== 200:
        return req.json()
    
def createJournal( userID: str, journalInfo ):
    
    req= requests.post( API_URL+ f"/journal/create/{userID}", json= dict(journalInfo) )
    res= req.status_code
    if res==200:
        return req.json()
    
def getJournal( userID: str ):
    
    req= requests.get( API_URL+ f"/journal/{userID}" )
    res= req.status_code
    if res==200:
        return req.json()
    
def getJournalAnalysis( userID: str, jid: str ):
    
    req= requests.get( API_URL+ f"/journal/sentiment/{userID}/{jid}" )
    res= req.status_code
    if res==200:
        return req.json()
    
def getSentimenatAnalysis( userID: str ):
    
    req= requests.get( API_URL+ f"/journal/sentiment/{userID}" )
    res= req.status_code
    if res==200:
        return req.json()