import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langdetect import detect

# Initialize the chat model
chat = ChatGroq(temperature=0.5, model_name="llama-3.1-70b-versatile", max_tokens=8000)

# Define system and human messages for both options
system_text = """You are an editor for a Marathi newspaper. Your task is to generate accurate Marathi news content from the following English news while preserving the original meaning and context. 
Use the language and style typically used in Marathi newspapers. Ensure that the Marathi text is grammatically correct and culturally appropriate. If certain terms or phrases are commonly used in English, retain them in English.
Do not exact translate; use your knowledge to adapt the content as needed."""

system_bullet = """You are an editor for a Marathi newspaper. Your task is to create a detailed and accurate Marathi news article based on the following bullet points, while preserving the original meaning and context. The article should be descriptive, using the language and style typically found in Marathi newspapers.
Ensure the Marathi text is grammatically correct and culturally appropriate. Do not simply copy the bullet points; instead, expand on them to create a coherent and engaging news story. You may add additional context and information to make the article more comprehensive and relatable. Use your knowledge and expertise to adapt the content as needed."""

human = "{text}"

# Create the prompt templates
prompt_text = ChatPromptTemplate.from_messages([("system", system_text), ("human", human)])
prompt_bullet = ChatPromptTemplate.from_messages([("system", system_bullet), ("human", human)])

# Define the Streamlit app
st.markdown("<h1 style='text-align: center;'>Marathi News Generator</h1>", unsafe_allow_html=True)

# Selection box for choosing the type of news generation
option = st.selectbox("Select the type of news generation:", ("Enter English News Text to Translate to Marathi", "Enter Marathi text for creating Marathi News Article"))

# Input text box
input_text = st.text_area("Enter English News Text or Bullet Points:", height=300)

if st.button("Generate Marathi News"):
    if len(input_text) < 50:
        st.error("Please enter at least 50 characters to generate the news.")
    else:
        if input_text:
            lang = detect(input_text)
            
            if option == "Enter English News Text to Translate to Marathi":
                if lang != "en":
                    st.warning("Please enter English text for Marathi news generation.")
                else:
                    with st.spinner("Please wait, we are generating Marathi News..."):
                        chain = prompt_text | chat
                        response = chain.invoke({"text": input_text})
                        
                        # Check if response has the content attribute
                        if hasattr(response, 'content'):
                            result = response.content
                        else:
                            result = str(response)
                        
                        # Remove extra blank lines
                        result = "\n".join(line for line in result.splitlines() if line.strip())
                        
                        # Display the result
                        # st.subheader("Generated Marathi News:")
                        st.subheader("The output has been generated, please download by clicking the button below.")
                        st.download_button(
                            label="Download Response",
                            data=result,
                            file_name="generated_marathi_news.txt",
                            mime="text/plain")

            elif option == "Enter Marathi text for creating Marathi News Article":
                if lang != "mr":
                    st.warning("Please enter only Marathi text to generate Marathi news article.")
                else:
                    with st.spinner("Please wait, we are generating Marathi News..."):
                        chain = prompt_bullet | chat
                        response = chain.invoke({"text": input_text})
                        
                        # Check if response has the content attribute
                        if hasattr(response, 'content'):
                            result = response.content
                        else:
                            result = str(response)
                        
                        # Remove extra blank lines
                        result = "\n".join(line for line in result.splitlines() if line.strip())
                        
                        # Display the result
                        # st.subheader("Generated Marathi News:")
                        st.subheader("The output has been generated, please download by clicking the button below.")
                        st.download_button(
                            label="Download Response",
                            data=result,
                            file_name="generated_marathi_news.txt",
                            mime="text/plain")

        else:
            st.error("Please enter some text to generate the news.")
