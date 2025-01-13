import streamlit as st
import datetime

from reqs import getJournal
from components.newJournal import newJournals

@st.dialog("Are your sure?")
def logoutAlert():
    col1, col2= st.columns(2)
    col1.button('Cancel', use_container_width= True)
    if col2.button('Confirm', type= 'primary',
                use_container_width= True):
        logout()
        
def logout()-> None:
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()


def navBar()-> None:
                
    # navbar
    statusCol, bttns= st.columns([0.6, 0.4], vertical_alignment= 'center')
    crttBtn, loutBttn= bttns.columns([0.7, 0.3])
    
    statusCol.info(f"{datetime.datetime.now().date()}")
    if crttBtn.button('Create a Journal', use_container_width= True,
                   type= 'primary'):
        newJournals()
    
    if loutBttn.button(':material/Logout:', help= ":red[Logout :material/Logout:]",
                    use_container_width= True):
        logoutAlert()