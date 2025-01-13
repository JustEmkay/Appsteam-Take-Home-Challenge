import streamlit as st
import datetime

from reqs import getSentimenatAnalysis



def sentimentView(selected)-> None:
    with st.container(border= True, height= 400):
        st.markdown("### Sentiment Analysis :material/Smart_Toy: ")
        
        if selected:
            result: dict= getSentimenatAnalysis( userID= st.session_state.auth['uid'],
                                                jidList= selected)
            st.markdown(selected)
            

        else:
            st.markdown("write one journal")
     