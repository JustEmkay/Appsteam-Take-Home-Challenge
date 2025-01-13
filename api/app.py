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
        
    
# @app.get("/journal/sentiment/{uid}")
# async def sentiment( uid: str, jidList: list[str] )-> dict:
    
#     Rjournals= selectedJournal(uid= uid, jids= jidList)
    
#     if Rjournals:
            
#         tempDict={}   
#         for key, jdata in Rjournals.items():
        
#             query: str= f"""
#             {datetime.datetime.fromtimestamp(jdata['created_date']).strftime("%Y-%m-%d")}
            
#             {jdata['journal']}
#             """
        
#             result= llm.ollamaRequest(user_query= query, prompt_template= PROMPT_TEMP )
#             tempDict.update({key: result['response']['message']['content']})
    
#         return {
#             'sentiment': tempDict
#             }
    
@app.get("/journal/sentiment/{uid}")
async def overallSentiment( uid: str )-> dict:
    
    jdata= getJournals(uid= uid)
    if jdata:
        # query= {}
        # for key, data in jdata:
        #     query 
        
        json_obj= json.dumps(jdata, indent= 2)
        
        response= llm.ollamaRequest(user_query= json_obj, prompt_template= SA_PROMPT )

    
    
    return {
        'sa': response['response']['message']['content'] 
    }