from fastapi import FastAPI, Query
from pydantic import BaseModel
import datetime, uuid, bcrypt
from database import *
from typing import Annotated, List


app= FastAPI()

# Schema
class registerInfo(BaseModel):
    username: str
    password: str
    question: str
    answer: str
    
class loginInfo(BaseModel):
    username: str
    password: str

class journalInfo(BaseModel):
    journal: str
    created_date: int
    
# password verifying function
def hash_pass( userPass: str ) -> str:
    pswd = userPass.encode('utf-8')
    return bcrypt.hashpw(pswd,bcrypt.gensalt())

def hash_verify( userPass: str, hashedPass: str ) -> bool:
    pswd = userPass.encode('utf-8')
    return bcrypt.checkpw(pswd,hashedPass)
    

# api requests
@app.get("/")
async def test(): 
    return {
        'print': "hello world"
    }
 
@app.post("/register")
async def registerUser( register: registerInfo )-> dict:
    
    # print(register.username)
    
    if verifyUser(username= register.username):
        return {
            'status': False,
            'msg': 'User Exist.'
        }
        
    if insertUser(uid= str(uuid.uuid1()), username= register.username,
                  password= hash_pass(register.password), q= register.question,
                  a= hash_pass(register.answer)):
        return {
            'status': True,
            'msg': 'Account created successfully.'
        }
           
@app.post("/verify")
async def verifyUser( login: loginInfo )-> dict: 

    # check for user and return uid
    checkUser: tuple= verifyUsers(username= login.username )
    if checkUser:
        # use the usrname and uid to get password as of tuple (ui, un, pwd)
        userCred: tuple= verifyUsers(username= login.username, uid= checkUser[0])
        
        if hash_verify( userPass= login.password, hashedPass= userCred[2]):
            
            return {
                'status': True,
                'msg': 'Login was successful.',
                'data': {
                    'username': login.username,
                    'uid': userCred[0]
                }
            }
        return {
            'status': False,
            'msg': 'User not found.'
        }
           
@app.post("/journal/create/{uid}")
async def createJournal( uid: str, journal: journalInfo )-> dict:

    jid: str= str(uuid.uuid1())
    
    if insertJournal( jid= jid, uid= uid,
                  journal= journal.journal,
                  created_date= journal.created_date):
        return {
            'status': True,
            'msg': 'Created new journal',
            'jid': jid
        }
    return {
        'status': True,
        'msg': 'Failed to create new journal.'
    }

@app.get("/journal/{uid}")
async def getallJournal( uid: str )-> dict:

    journals: dict= getJournals(uid= uid)
    
    print("api:\n",journals)
    
    return {
        "journals": journals
    }
    
@app.get("/journal/sentiment/{uid}/{jidList}")
async def sentiment( uid: str, jidList )-> dict:
    
    print(jidList)
    
    return {
        'sentiment': 'lol'
    }