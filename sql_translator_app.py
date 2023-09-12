import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Define your function
def my_function(text):
    # You can replace this with your custom text processing logic
    return text.upper()

# Streamlit app header
st.title("SQL translator app")

# Text input field
user_input = st.text_input("Question:")

# Check if the user has entered any text
if user_input:
    # Apply your custom function to the input text
    result = my_function(user_input)
    
    # Display the transformed text
    st.text("SQL query:")
    st.write(result)