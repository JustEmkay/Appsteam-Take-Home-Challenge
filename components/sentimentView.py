import streamlit as st

from reqs import getSentimenatAnalysis, getJournalAnalysis
from components.functions import hashList


def check_sentimentData( selected: list )-> str:
    
    hashKey: str= hashList(selectedList= selected)
    
    if hashKey in st.session_state.sentiment:
        return hashKey


# OVERALL SENNTIMENT ANALYSIS
def sentimentView( )-> None:
    
    # req overall Sentiment analysis of users journals
    if st.session_state.reloadData['sa']:
        
        result: dict= getSentimenatAnalysis(userID= st.session_state.auth['uid'])
        if result:
            st.session_state.sentiment['sa']= result['sa']
            st.session_state.reloadData['sa']= False
            st.rerun()    
    
    with st.container(border= True, height= 400):
        
        st.markdown("##### Sentiment Analysis :material/Smart_Toy: ")
        st.divider()
        
        st.markdown(st.session_state.sentiment['sa'])
        
        
        
# JOURNAL SENETMENT ANALYSIS 
def eachSentimental(jid: str)-> None:
    with st.container(border= True):
        
        if jid not in st.session_state.sentiment['js']:

            response= getJournalAnalysis(userID= st.session_state.auth['uid'], jid= jid)
            if response:
                st.session_state.sentiment['js'].update({ response['jid']: response['js'] })
                
                
        st.markdown(f"{st.session_state.sentiment['js'][jid]}")