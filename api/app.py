from fastapi import FastAPI
from pydantic import BaseModel
import datetime, uuid, bcrypt, json
from database import *

from llm import OllamaLLM
from prompt import JS_PROMPT, SA_PROMPT 


app= FastAPI()
llm= OllamaLLM( model_name= "llama3.2:1b" )

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
def hashPassword( userPass: str, hashedPass: str= None ) -> bool:
    pswd = userPass.encode('utf-8')
    if not hashedPass:
        return bcrypt.hashpw(pswd,bcrypt.gensalt())
    return bcrypt.checkpw(pswd,hashedPass)
    

# api requests
@app.get("/")
async def test(): 
    return {
        'print': "hello world"
    }
 
@app.post("/register")
async def registerUser( register: registerInfo )-> dict:
    
    print(register.username)
    
    if verifyUsers(username= register.username):
        return {
            'status': False,
            'msg': 'User Exist.'
        }
        
    if insertUser(uid= str(uuid.uuid1()), username= register.username,
                  password= hashPassword(userPass= register.password), q= register.question,
                  a= hashPassword(register.answer)):
        return {
            'status': True,
            'msg': 'Account created successfully.'
        }
           
@app.post("/verify")
async def userVerify( login: loginInfo )-> dict: 

    # check for user and return uid
    checkUser: tuple= verifyUsers(username= login.username )
    if checkUser:
        # use the usrname and uid to get password as of tuple (ui, un, pwd)
        userCred: tuple= verifyUsers(username= login.username, uid= checkUser[0])
        
        if hashPassword( userPass= login.password, hashedPass= userCred[2]):
            
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
    
@app.get("/journal/sentiment/{uid}/{jid}")
async def sentiment(uid: str, jid: str)-> dict:
    
    jdata= selectedJournal( uid= uid, jids= [jid] )
    
    if jdata:
        query: str= f""" 
        {datetime.datetime.fromtimestamp(jdata[jid]['created_date']).strftime("%d/%m/%Y")}
        
        {jdata[jid]['journal']}
        """

        response= llm.ollamaRequest(prompt_template= JS_PROMPT, user_query= query)
        
        return {
            'jid': jid,
            'js': response['response']['message']['content']
        }
        
    
@app.get("/journal/sentiment/{uid}")
async def overallSentiment( uid: str )-> dict:
    
    jdata= getJournals(uid= uid)
    if jdata:

        json_obj= json.dumps(jdata, indent= 2)
        
        response= llm.ollamaRequest(user_query= json_obj, prompt_template= SA_PROMPT )

    
    
    return {
        'sa': response['response']['message']['content'] 
    }
    
    
@app.put("/journal/update/{uid}/{jid}")
async def update( uid: str, jid: str, journal: journalInfo )-> dict:
    
    response= updateJournal( userID= uid, journalID= jid,
                            journal= journal.journal,
                            updated_date= journal.created_date)
    if response:
        return {
            'status': True,
            'msg': 'updated successfully.'
        }
    return {
        'status': False,
        'msg': 'failed to update.' 
    }
        
        
@app.delete("/journal/delete/{uid}/{jid}")
async def delete( uid: str, jid: str )-> dict:
    
    response= deleteJournal( userID= uid, journalID= jid )
    if response:
        return {
            'status': True,
            'msg': 'Deleted successfully.'
        }
    return {
        'status': False,
        'msg': 'failed to Deletion.' 
    }