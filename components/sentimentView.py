import streamlit as st

from reqs import getSentimenatAnalysis, getJournalAnalysis


# OVERALL SENNTIMENT ANALYSIS
def sentimentView( )-> None:
    
    # req overall Sentiment analysis of users journals
    with st.container(border= True, height= 400):
        
        
            if st.session_state.reloadData['sa']:
                with st.status(" Connecting API... ", expanded=True) as status:
                    status.update(label="Generating Sentimental Analysis...", state="running", expanded=False)         
                    result: dict= getSentimenatAnalysis(userID= st.session_state.auth['uid'])
                    if result:
                        status.update(label="Completed", state="complete", expanded=False)         
                        st.session_state.sentiment['sa']= result['sa']
                        st.session_state.reloadData['sa']= False
                        st.rerun()    
            
                
            st.markdown("##### Sentiment Analysis :material/Smart_Toy: ")
            # st.divider()
            st.markdown(st.session_state.sentiment['sa'])
            # status.update(label="Sentiment Analysis :material/Smart_Toy:", state="complete", expanded=True)
            
        
        
# JOURNAL SENETMENT ANALYSIS 
def eachSentimental( jid: str )-> None:
    
    with st.container(border= True):
        
        if not st.session_state.journals:
            st.markdown("No Journals found")
        else:
            if jid not in st.session_state.sentiment['js']:

                response= getJournalAnalysis(userID= st.session_state.auth['uid'], jid= jid)
                if response:
                    st.session_state.sentiment['js'].update({ response['jid']: response['js'] })
                    
                    
            st.markdown(f"{st.session_state.sentiment['js'][jid]}")