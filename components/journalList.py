import streamlit as st

from reqs import getJournal
from components.functions import timestamp2Datetime, filterJournal
from components.sentimentView import eachSentimental



# JOURNAL-LIST CONTAINER
def JournalList()-> None:
    
    filterOpt: list= [ 'Day', 'Week', 'Month', 'Year', 'All' ]
    
    # reload journal list 
    if st.session_state.reloadData['journal']:
        result= getJournal(st.session_state.auth['uid'])
        if result:
            st.session_state.journals= result['journals']
            st.session_state.reloadData['journal']= False
            st.rerun()
            
    # journal LIST container         
    with st.container(border= True, height= 400):
        
        if st.session_state.journals:
            
            selection = st.segmented_control("Filter Journal",
                                             filterOpt, default= 'All')

            fltrJ: dict= filterJournal(st.session_state.journals, option= selection)

            for key, data in fltrJ.items():
                
                with st.expander(f" :green[:material/Calendar_Month: {timestamp2Datetime(data['created_date'])}]"):
                    st.markdown(data['journal'], help= f"created on:{timestamp2Datetime(data['created_date'])}")
                    if st.checkbox("Generate Sentiment analysis",
                                   help= ":material/Smart_Toy: Generate AI Sentiment Analysis: Emotion detection and Polarity classification ",
                                   key= key, value= False):

                        # JOURNAL SENTIMENTAL CONTAINER
                        eachSentimental(key)    
                
                
                    
        else:
            st.text('no journal list found')
        