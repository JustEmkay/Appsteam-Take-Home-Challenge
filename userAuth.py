import streamlit as st
from pydantic import BaseModel
from reqs import registerUser, verifyUser
import time

# schema
class userInfo(BaseModel):
    username: str
    password: str
    question: str
    answer: str

class loginInfo(BaseModel):
    username: str
    password: str
    

# Dialog Box - Registration
@st.dialog("Register Your Account")
def registrationDialog()->None:
    
    username: str= st.text_input("username",
                                placeholder= "Ente your username",
                                label_visibility= "collapsed")
    
    password: str= st.text_input("password", 
                                placeholder= "create new password",
                                label_visibility= "collapsed",
                                type= "password")

    cpassword: str= st.text_input("confirm password", 
                                placeholder= "re-enter password",
                                label_visibility= "collapsed",
                                type= "password")
    
    question: str= st.text_input("Question", 
                                placeholder= "Please Enter a question",
                                label_visibility= "collapsed")
    
    answer: str= st.text_input("Answer", 
                                placeholder= "Enter answaer for above question",
                                label_visibility= "collapsed",
                                type= "password")

    alert= st.empty() #placeholder for alert

    if password != cpassword:
        alert.warning("Password Not Equal")     
    elif not username and (password == cpassword) and \
    question and answer:
        alert.warning("Fill all fields")
               

    
    if st.button('create account',
                                disabled= False if (password and cpassword) and username else True,
                                use_container_width= True):
            
            registerInfo= userInfo(username= username,
                                   password= password,
                                   question= question,
                                   answer= answer)
            
            result: dict= registerUser(registerInfo)
            if result['status']:
                alert.success(result['msg'])
            else:
                alert.warning(result['msg'])

# login page
def loginPage()-> None:
    
    # textbox
    username: str= st.text_input("Username")
    password: str= st.text_input("Password", type="password")
    
    alert= st.empty()
    
    blnk, btn1, btn2= st.columns([2,1,1])
    
    if btn1.button("Register", use_container_width = True):
        registrationDialog()
        
    if btn2.button("Login", type="primary",
                use_container_width = True):
        if not username or not password:
            alert.warning("Fill all the fields.", icon='⚠')
        else:
            
            login= loginInfo(username= username, password= password)
            result: dict= verifyUser(login)
            
            if result['status']:
                alert.success(result['msg'])
                with st.status('Loading main page...') as status:
                    time.sleep(0.5)
                    status.update(label="Setting user..",
                                  state="running",
                                  expanded=False)
                    st.session_state.auth.update(
                        result['data']
                    )
                    time.sleep(1)
                    status.update(label="Redirecting to main page....",
                                  state="complete",
                                  expanded=False)
                    st.rerun()
                    
            else:
                alert.error(result['msg'])