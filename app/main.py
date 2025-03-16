import streamlit as st
from sidebar import sidebar
import re ,os
from fpdf import FPDF
from patent_download import PatentDownloader
from llm import get_chain

def set_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')

def prepare_pdf_data():
    msgs = st.session_state.get("msgs", None)
    
    if not msgs or not msgs.messages:
        st.warning("No conversation history to save!")
        return None

    # Create PDF in memory
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add title to PDF
    pdf.cell(200, 10, "Chat History", ln=True, align="C")
    pdf.ln(10)

    # Add messages to the PDF
    for msg in msgs.messages:
        role = "User" if msg.type == "human" else "AI"
        pdf.multi_cell(0, 10, f"{role}: {msg.content}")
        pdf.ln(5)
    pdf_output = pdf.output(name="chat_history.pdf", dest="S").encode("latin1")
    return pdf_output

def extract_patent_number(patent_link: str):
    pattern = r"/patent/([^/?#]+)"
    match = re.search(pattern, patent_link)
    if match:
        return match.group(1)
    else:
        return None
    
def run_app():
    st.title('Chat with Google Patents!')
    st.subheader(
        "Chat with Google Patent"
    )
    sidebar()
    if not st.session_state.get("open_api_key_configured"):
        st.error("Please configure your API Keys!")
    if not st.session_state.get("patent_link_configured"):
        st.error("Please set the patent link!")
    
    elif (st.session_state.get("open_api_key_configured") 
            and st.session_state.get("patent_link_configured")):
        patent_link = st.session_state.get("PATENT_LINK")
        patent_number = extract_patent_number(patent_link)
        st.write("Patent number: ", patent_number)
        pdf_path = os.path.join("patents", f"{patent_number}.pdf")
        if os.path.isfile(pdf_path):
            st.write("File already downloaded.")
        else:
            downloader = PatentDownloader()
            downloader.download(patent_number)
            st.write("File downloaded.")
        
        if "chain" not in st.session_state:  # Only load once
            spinner_placeholder = st.empty()
            with spinner_placeholder, st.spinner("Loading model..."):
                st.session_state["chain"] = get_chain(file_name=pdf_path)
            spinner_placeholder.empty()

        chain = st.session_state["chain"]
            
        msgs = st.session_state["msgs"]
        for msg in msgs.messages:
            st.chat_message(msg.type).write(msg.content)
      
        col1, col2 = st.columns([100, 1])  # Input and Button side by side
        with col1:
            if prompt := st.chat_input():
                st.chat_message("human").write(prompt)

                with st.spinner("Thinking..."):
                    #new messages are saved to history automatically by Langchain during run
                    try:
                        retrieval_res = st.session_state["retriever"].invoke(prompt)
                    except Exception as e:
                        st.error(f"Error retrieving context: {str(e)}")
                        retrieval_res = ""
                    response = chain.stream({"user_input": prompt,
                                            "context":retrieval_res},
                                            config={"configurable": {"session_id": "any"}})
                
                with st.chat_message("ai"):
                    st.write_stream(response)
        
        with col2:
           dnl_btn = st.download_button(
            type = "secondary",
            label="",
            use_container_width=False,
            data= prepare_pdf_data(),
            file_name="chat_history.pdf",
            icon=":material/download:"
        )

    
if __name__ == "__main__":

    st.set_page_config(
        page_title="Chat with Google Patent",
        page_icon="📖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # Inject custom CSS to set the width of the sidebar
    st.markdown(
        """
        <style>
            section[data-testid="stSidebar"] {
                width: 400px !important; # Set the width to your desired value
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    run_app()