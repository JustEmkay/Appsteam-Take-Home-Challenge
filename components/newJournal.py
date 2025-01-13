import streamlit as st
import datetime, time
from pydantic import BaseModel

from reqs import createJournal

# schema
class journals(BaseModel):
    journal: str
    created_date: int


def preView( journal: str )-> None:
    with st.container(border= True, height= 400):
        st.markdown(f"""{journal if journal else 'please write soemthing...'}""")


@st.dialog("Personal Journal", width= 'large')
def newJournals()-> None:
    st.subheader("create a Journal", divider= True,
    anchor= False)
    
    wJrnl, pJrnl= st.columns(2)
    journal: str= wJrnl.text_area("Enter here",
                                placeholder= "Write how was your day?",
                                height=400)
    
    with pJrnl.container(border= True, height= 430):
        st.markdown(f"""{journal if journal else 'please write something...'}""",
                    unsafe_allow_html= True)

    char, prv, crt= st.columns([2, 1, 1])
    char.text(f"You wote {len(journal)} characters.")
    
    if prv.button(":material/Preview:",
                    help=":blue[Preview :material/Preview:]",
                    use_container_width= True, disabled= True):
        ...
        
    if crt.button("create :material/Add_Circle:",
                    help= ":green[create new journal :material/Add_Circle:]",
                    use_container_width= True,
                    type="primary"):
        if journal:
            journlInfo= journals(journal= journal,
                                 created_date= int(datetime.datetime.now().timestamp()))
            createJournal( st.session_state.auth['uid'],
                          journalInfo= journlInfo )
            st.session_state.reloadData['journal']= True
            time.sleep(1)
            st.rerun()
            # st.write(journlInfo)