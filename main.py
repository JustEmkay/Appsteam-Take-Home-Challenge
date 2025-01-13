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
    'journal': True
}

if 'journals' not in st.session_state: st.session_state.journals= {}

if 'sentiment' not in st.session_state: st.session_state.sentiment= {}

#main
def main() -> None:
    
    navBar()
    
    jlst, smry= st.columns([0.7, 0.3])
    
    with jlst.container():
        selected= JournalList()
        
    with smry.container():
        sentimentView(selected)
    
    
    
if __name__ == "__main__":
    
    st.title("Journal x LLM 🦙", anchor= False)
    
    if st.session_state.auth['uid']:
        main()
    else:
        loginPage()