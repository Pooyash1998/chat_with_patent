import streamlit as st

def set_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key
    st.session_state["open_api_key_configured"] = True
    print('OPENAI API key is Configured Successfully!')

def sidebar():
    with st.sidebar:
      st.subheader(
          "Configurations"
      )

      if 'model_name' not in st.session_state:
          st.session_state['model_name'] = "gpt-4o" 
      with st.expander("Configuration", expanded=True):
          model_name = st.text_input("Enter the AI model name:",
                                    key='model_name',
                                    help="Enter the name of the model from openai that you want to use.")
          api_key = st.text_input("Enter the API key:",
                                  key='api_key',
                                  type='password',
                                  help="Enter the API key from openai.",
                                  value=st.session_state.get("OPEN_API_KEY", ""))
          if api_key:
              st.session_state['OPEN_API_KEY'] = api_key
              set_api_key(api_key)
            
          if not st.session_state.get("open_api_key_configured"):
              st.error("Please configure your Open API key!")
          else:
              st.markdown("Open API Key Configured!")
          
          patent_link = st.text_input(
              "Google Patent Link",
              type="default",
              placeholder="Paste the Google patent link here",
              help="You can goto patents.google.com to get the link from the browser.",
              value=st.session_state.get("PATENT_LINK", ""),
          )
          if patent_link:
              st.session_state["PATENT_LINK"] = patent_link
              st.session_state["patent_link_configured"] = True
          
          if not st.session_state.get("patent_link_configured"):
              st.error("Please configure your Google Patent Link!")
          else:
              st.markdown("Google Patent Link Configured!")
        
          
