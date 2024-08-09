import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langdetect import detect
import re

# Add logo and header in a container

# Set the page configuration
st.set_page_config(
    page_title="Marathi News Generator",  # Title of the web page with smiley
    page_icon="favicon.png",
    layout="centered"  # Layout of the page
)
 
 


# Path to your logo image
logo_path = "cloudmantra_logo1.png"

# Create columns for logo and content
col1, col2 = st.columns([1, 5])  # Adjust the column widths as needed

with col1:
    st.image(logo_path, width=110)  # Adjust the width as needed

# Initialize the chat models
chat_text = ChatGroq(temperature=0.15, model_name="llama-3.1-70b-versatile", max_tokens=8000)
chat_bullet = ChatGroq(temperature=0.18, model_name="llama-3.1-70b-versatile", max_tokens=8000)
chat_evaluate = ChatGroq(temperature=0.5, model_name="llama-3.1-70b-versatile", max_tokens=8000)

# Define system and human messages for both options
system_text = """You are an editor for a Marathi newspaper. Your task is to generate accurate Marathi news content from the following English news while preserving the original context. 
Use the language and style typically used in Marathi newspapers. Ensure that the Marathi text is grammatically correct and culturally appropriate. If certain terms or phrases are commonly used in English, retain them in English.
Do not exact translate; use your knowledge to adapt the content as needed. """


system_bullet_40_100="""You are an editor for a Marathi newspaper. Generate a clear and detailed news article in Marathi based on the provided information. Ensure the article is factually accurate and includes a thorough explanation of the events described. Aim for a length of approximately 100 to 150 words, and avoid repetition. Add any relevant factual details to provide a comprehensive view of the situation. The final article should be natural, coherent, and informative."""

system_bullet_101_150="""You are an editor for a Marathi newspaper. Generate a clear and detailed news article in Marathi based on the provided information. Ensure the article is factually accurate and includes a thorough explanation of the events described. Aim for a length of approximately 150 to 200 words, and avoid repetition. Add any relevant factual details to provide a comprehensive view of the situation. The final article should be natural, coherent, and informative."""
system_bullet_151_200="""You are an editor for a Marathi newspaper. Generate a clear and detailed news article in Marathi based on the provided information. Ensure the article is factually accurate and includes a thorough explanation of the events described. Aim for a length of approximately 200 to 250 words, and avoid repetition. Add any relevant factual details to provide a comprehensive view of the situation. The final article should be natural, coherent, and informative."""
 
system_bullet_201_more="""You are an editor for a Marathi newspaper. Generate a clear and detailed news article in Marathi based on the provided information. Ensure the article is factually accurate and includes a thorough explanation of the events described. Aim for a length of approximately 250 or more words, and avoid repetition. Add any relevant factual details to provide a comprehensive view of the situation. The final article should be natural, coherent, and informative."""

system_tags = """You are an expert in SEO and keyword optimization. I need your help to generate a list of highly relevant SEO tags for an Marathi news article. from marathi news provided.
The SEO tags should capture various aspects of the article's topic to enhance its search engine ranking. Please ensure the tags are comprehensive, cover different angles of the content, and are naturally integrated without appearing forced. Provide the tags in English only, formatted as a list."""

human = "{text}"

# Create the prompt templates
prompt_text = ChatPromptTemplate.from_messages([("system", system_text), ("human", human)])
prompt_bullet_40_100= ChatPromptTemplate.from_messages([("system", system_bullet_40_100), ("human", human)])
prompt_bullet_101_150= ChatPromptTemplate.from_messages([("system", system_bullet_101_150), ("human", human)])
prompt_bullet_151_200= ChatPromptTemplate.from_messages([("system", system_bullet_151_200), ("human", human)])
prompt_bullet_201_more= ChatPromptTemplate.from_messages([("system", system_bullet_201_more), ("human", human)])

prompt_tags = ChatPromptTemplate.from_messages([("system", system_tags), ("human", human)])

# Define the Streamlit app
st.markdown("<h1 style='text-align: center;'>Marathi News Generator</h1>", unsafe_allow_html=True)

 
# Selection box for choosing the type of news generation
option = st.selectbox("Select the type of news generation:", 
                      ["Enter English News Text to Translate to Marathi", 
                       "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या",
                       "SEO keywords तयार करण्यासाठी मराठीत माहिती द्या"])
 

# Input text box label based on selected option
if option == "Enter English News Text to Translate to Marathi":
    input_label = "Enter your text below:"
elif option == "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या":
    input_label = "खालील बॉक्समध्ये तुमचा मजकूर प्रविष्ट करा"
else:  # Handles the third condition
    input_label = "खालील बॉक्समध्ये तुमचा मजकूर प्रविष्ट करा"

input_text = st.text_area(input_label, height=300)

 

# Button and result handling based on option selected
if option == "SEO keywords तयार करण्यासाठी मराठीत माहिती द्या":
    if st.button("Generate SEO Keywords"):
        if len(input_text) < 50:
            st.error("कृपया SEO keywords तयार करण्यासाठी किमान ५० अक्षर प्रविष्ट करा.")
        else:
            lang = detect(input_text)
            if lang != "mr":
                st.warning("कृपया मराठीत माहिती द्या")
            else:
                with st.spinner("कृपया थांबा, आम्ही SEO keywords तयार करत आहोत..."):
                    chain = prompt_tags | chat_text
                    response = chain.invoke({"text": input_text})

                    # Check if response has the content attribute
                    if hasattr(response, 'content'):
                        result = response.content
                    else:
                        result = str(response)

                    # Prepare the combined text
                    combined_result = f"Input Text:\n{input_text}\n\nOutput Keywords:\n{result}"

                    # Display the result
                    st.subheader("SEO keywords तयार झाले आहेत, कृपया खाली दिलेल्या बटणावर क्लिक करून डाउनलोड करा.")
                    st.download_button(
                        label="Download Response",
                        data=combined_result,
                        file_name="generated_seo_keywords.txt",
                        mime="text/plain")
                     

elif option == "Enter English News Text to Translate to Marathi":
    if st.button("Generate Marathi News"):
        if len(input_text) < 50:
            st.error("Please enter at least 50 characters to generate the news.")
        else:
            lang = detect(input_text)
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
                    result= re.sub(r'\s+', ' ', result).strip()
                    combined_result = f"Input Text:\n{input_text}\n\nGenerated Marathi News:\n{result}"
                    # Display the result
                    st.subheader("The output has been generated, please download by clicking the button below.")
                    st.download_button(
                        label="Download Response",
                        data=combined_result,
                        file_name="generated_marathi_news.txt",
                        mime="text/plain")
                    
                    

elif option == "मराठी बातमी लेख तयार करण्यासाठी मराठीत माहिती द्या":
    if st.button("Generate Marathi News"):
        if len(input_text.split()) < 40:
            st.error("कृपया बातमी तयार करण्यासाठी किमान ४0 शब्द प्रविष्ट करा.")
        else:
            lang = detect(input_text)
            if lang != "mr":
                st.warning("कृपया मराठीत माहिती द्या.")
            else:
                with st.spinner("कृपया थांबा, आम्ही मराठी बातमी लेख तयार करत आहोत..."):
                    if 40 <= len(input_text.split()) <= 100:
                        chain = prompt_bullet_40_100 | chat_bullet
                    elif 101 <= len(input_text.split()) <= 150:
                        chain = prompt_bullet_101_150 | chat_bullet
                    elif 151 <= len(input_text.split()) <= 200:
                        chain = prompt_bullet_151_200 | chat_bullet
                    else:
                        chain = prompt_bullet_201_more | chat_bullet

                    response = chain.invoke({"text": input_text})
                    

                    # Check if response has the content attribute
                    if hasattr(response, 'content'):
                        result = response.content
                    else:
                        result = str(response)

                    # Remove extra blank lines
                    result = "\n".join(line for line in result.splitlines() if line.strip())
                    result= re.sub(r'\s+', ' ', result).strip()
                    
                    combined_result = f"Input Text:\n{input_text}\n\nGenerated Marathi News:\n{result}"


                    # Display the result
                    st.subheader("तुमच्या माहितीच्या आधारे लेख तयार झाला आहे, कृपया खालील बटणावर क्लिक करून डाउनलोड करा.")
                    st.download_button(
                        label="Download Response",
                        data=combined_result,
                        file_name="generated_marathi_news_article.txt",
                        mime="text/plain")
                    
                    
