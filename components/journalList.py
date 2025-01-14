import streamlit as st
import time

from reqs import getJournal, deleteJournal
from components.functions import timestamp2Datetime, filterJournal
from components.sentimentView import eachSentimental
from components.newJournal import editJournal

@st.dialog("Are you sure?")
def deleteAlert(jid)-> None:
    
    st.write("Do you want to delete this journal?")
    if st.button("Confirm", type= 'primary'):
        alert= st.empty()
        response= deleteJournal(userID= st.session_state.auth['uid'],
                                journalID= jid)
        if response:
            alert.success(response['msg'])
            st.session_state.reloadData['journal']= True
            time.sleep(1)
            st.rerun()
                        
        else:
            alert.error(response['msg'])
           

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
            # JOURNAL LIST EXPANDER
            for key, data in fltrJ.items():
                
                
                with st.expander(f" :green[:material/Calendar_Month: {timestamp2Datetime(data['created_date'])}]"):
                    
                    st.markdown(data['journal'], help= f"created on:{timestamp2Datetime(data['created_date'])}")
                    
                    genCol, dltBttn, editBttn= st.columns([3, 0.5, 0.5])
                    
                    # CHECKBOX
                    if genCol.checkbox("Generate Sentiment analysis",
                                   help= ":material/Smart_Toy: Generate AI Sentiment Analysis: Emotion detection and Polarity classification ",
                                   key= key, value= False):

                        # JOURNAL SENTIMENTAL CONTAINER
                        eachSentimental(key)
                    
                    # DELETE BUTTTON
                    if dltBttn.button(":material/Delete:", key= key+"dlt",
                                      help= ":red[Delete :material/Delete:]",
                                      use_container_width= True):
                        
                        # Delete Alert Box
                        deleteAlert( jid= key)
                        
                        
                    # EDITT BUTTON
                    if editBttn.button(":material/Edit_Note:", key= key+"bttn",
                                       help= ":material/Edit_Note: Edit journal",
                                       use_container_width= True):
                        # EDit journal dialogbox
                        editJournal( jid= key, journal= data)                
                
                    
        else:
            st.text('no journal list found')
        