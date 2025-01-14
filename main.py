import streamlit as st

from userAuth import loginPage
from components.navbar import navBar
from components.sentimentView import sentimentView
from components.journalList import JournalList

# session states
if 'auth' not in st.session_state: st.session_state.auth= {
    'uid': None,
    'username': None
}

if 'reloadData' not in st.session_state: st.session_state.reloadData= {
    'journal': True,
    'sa': True
}

if 'journals' not in st.session_state: st.session_state.journals= {}

# Stores journal sentiment analysis(js: dict) data and  overall sentimenl analysis(sa: str)
if 'sentiment' not in st.session_state: st.session_state.sentiment= {
    'js': {},
    'sa': ''
}

#main
def main() -> None:
    
    navBar() #Navigation
    
    jlst, smry= st.columns([0.6, 0.4])
    
    with jlst.container():
        JournalList()
        
    with smry.container():
        sentimentView()
    
    
    
if __name__ == "__main__":
    
    st.title("Journal x LLM 🦙", anchor= False)
    if st.session_state.auth['uid']:
        main()
    else:
        loginPage()