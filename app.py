import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langdetect import detect

# Add logo and header in a container

# Path to your logo image
logo_path = "cloudmantra_logo1.png"

# Create columns for logo and content
col1, col2 = st.columns([1, 5])  # Adjust the column widths as needed

with col1:
    st.image(logo_path, width=110)  # Adjust the width as needed

# Initialize the chat models
chat_text = ChatGroq(temperature=0.5, model_name="llama-3.1-70b-versatile", max_tokens=8000)
chat_bullet = ChatGroq(temperature=0.05, model_name="llama-3.1-70b-versatile", max_tokens=8000)

# Define system and human messages for both options
system_text = """You are an editor for a Marathi newspaper. Your task is to generate accurate Marathi news content from the following English news while preserving the original meaning and context. 
Use the language and style typically used in Marathi newspapers. Ensure that the Marathi text is grammatically correct and culturally appropriate. If certain terms or phrases are commonly used in English, retain them in English.
Do not exact translate; use your knowledge to adapt the content as needed."""

system_bullet = """
You are an editor for a Marathi newspaper. Rewrite the provided information into a clear and concise news article in Marathi. Ensure the article is factually accurate and does not include any information not mentioned in the input. Do not add any information that is not provided. Avoid repetition and unnecessary details. Use the usual language and style of Marathi newspapers. Make sure the text is grammatically correct and descriptive. The article should be between 150 and 250 words, depending on the detail in the input. 
"""
human = "{text}"

# Create the prompt templates
prompt_text = ChatPromptTemplate.from_messages([("system", system_text), ("human", human)])
prompt_bullet = ChatPromptTemplate.from_messages([("system", system_bullet), ("human", human)])

# Define the Streamlit app
st.markdown("<h1 style='text-align: center;'>Marathi News Generator</h1>", unsafe_allow_html=True)

# Initialize session state
if 'option' not in st.session_state:
    st.session_state.option = "Enter English News Text to Translate to Marathi"
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

# Selection box for choosing the type of news generation
option = st.selectbox("Select the type of news generation:", 
                      ["Enter English News Text to Translate to Marathi", 
                       "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या"],
                      index=["Enter English News Text to Translate to Marathi", 
                             "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या"].index(st.session_state.option))

# Check if the selected option has changed
if option != st.session_state.option:
    st.session_state.option = option
    st.session_state.input_text = ""  # Clear the input text
    st.experimental_rerun()  # Refresh the page to clear the input field

# Input text box
input_label = "Enter your text below:" if option == "Enter English News Text to Translate to Marathi" else "खालील बॉक्समध्ये तुमचा मजकूर प्रविष्ट करा"
input_text = st.text_area(input_label, value=st.session_state.input_text, height=300)

# Update session state with current input
st.session_state.input_text = input_text

if st.button("Generate Marathi News"):
    # Automatically clear cache
    st.cache_data.clear()
    st.cache_resource.clear()
    
    if len(input_text) < 50:
        if option == "Enter English News Text to Translate to Marathi":
            st.error("Please enter at least 50 characters to generate the news.")
        else:
            st.error("कृपया बातमी तयार करण्यासाठी किमान ५० अक्षरे प्रविष्ट करा.")
    else:
        if input_text:
            lang = detect(input_text)
            
            if option == "Enter English News Text to Translate to Marathi":
                if lang != "en":
                    st.warning("Please enter only English text for Marathi news article.")
                else:
                    with st.spinner("Please wait, we are generating Marathi news article..."):
                        chain = prompt_text | chat_text
                        response = chain.invoke({"text": input_text})
                        
                        # Check if response has the content attribute
                        if hasattr(response, 'content'):
                            result = response.content
                        else:
                            result = str(response)
                        
                        # Remove extra blank lines
                        result = "\n".join(line for line in result.splitlines() if line.strip())
                        
                        # Display the result
                        st.subheader("The output has been generated, please download by clicking the button below.")
                        st.download_button(
                            label="Download Response",
                            data=result,
                            file_name="generated_marathi_news.txt",
                            mime="text/plain")

            elif option == "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या":
                if lang != "mr":
                    st.warning("कृपया मराठीत माहिती द्या.")
                else:
                    with st.spinner("कृपया थांबा, आम्ही मराठी बातमी लेख तयार करत आहोत..."):
                        chain = prompt_bullet | chat_bullet
                        response = chain.invoke({"text": input_text})
                        
                        # Check if response has the content attribute
                        if hasattr(response, 'content'):
                            result = response.content
                        else:
                            result = str(response)
                        
                        # Remove extra blank lines
                        result = "\n".join(line for line in result.splitlines() if line.strip())
                        
                        # Display the result
                        st.subheader("मराठी मजकूर तयार झाला आहे, कृपया खाली दिलेल्या बटणावर क्लिक करून डाउनलोड करा.")
                        st.download_button(
                            label="Download Response",
                            data=result,
                            file_name="generated_marathi_news.txt",
                            mime="text/plain")

        else:
            st.error("Please enter some text to generate the news.")
