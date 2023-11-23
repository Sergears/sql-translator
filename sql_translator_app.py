import streamlit as st
import requests
import time
import typing
from typing import List

model_id = "sergears/sql-translator"
api_token = st.secrets["HUGGING_FACE_API_KEY"]

def make_input_string(question: str, table_columns: List[str]) -> str:
    """
    Helper function to combine natural language question with table column names, and add prefixes
    """

    question_prefix = "Translate English to SQL: "
    table_prefix = ". Table column names: "
    question_input = question_prefix + question
    table_input = table_prefix + ', '.join(table_columns)
    return question_input + table_prefix

def query(payload, model_id, api_token):
    headers = {"Authorization": f"Bearer {api_token}"}
    API_URL = f"https://api-inference.huggingface.co/models/{model_id}"
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def translate_and_show_result(input_data):
    """
    Print response if successful, else if model is loading retry query in a few seconds
    Example of successful response: [{'generated_text': 'SELECT car FROM table WHERE price > 100'}]
    Example of model loading response: {'error': 'Model t5-small is currently loading', 'estimated_time': 20.0}
    """
    loading_time = 0
    attemt_delay_sec = 5
    max_loading_time = 60
    while True:
        response = query(input_data, model_id, api_token)
        if type(response) is list and len(response) > 0 and type(response[0]) is dict and 'generated_text' in response[0].keys():
            generated_text = response[0]['generated_text']
            st.code(generated_text, language="sql")
            break
        elif type(response) is dict and 'error' in response.keys() and response['error'].split()[-1] == 'loading':            
            loading_time += attemt_delay_sec
            if loading_time > max_loading_time:
                st.write('Model loading is taking too long, please try again later')
                break
            with st.spinner(text='Model is loading...'):
                time.sleep(attemt_delay_sec)
        else:
            st.write('Unknown response format:', str(response))
            break

#########################
# Functions needed to dynamically add input fields

def add_field():
    st.session_state.fields_size += 1
    st.session_state.fields.append("")

def delete_field(index):
    st.session_state.fields_size -= 1
    del st.session_state.fields[index]
    del st.session_state.deletes[index]

if "fields_size" not in st.session_state:
    st.session_state.fields_size = 0
    st.session_state.fields = []
    st.session_state.deletes = []

#########################
# UI part

st.title("Translate natural language to an SQL query")

with st.expander("ℹ️ - About this app", expanded=True):
    st.write(
        """     
        -   This app is an easy-to-use interface for English to SQL translation, built on top [Hugging Face](https://huggingface.co/docs/transformers/index) transformer library.
        -   Example: 
            - Question `Show who won the 1962 prize for literature`
            - Table columns
                - `year`
                - `subject`
                - `winner` 
            - Result: `SELECT winner FROM table WHERE year = 1962 AND subject = literature`
        -   Try it yourself 😊
	    """
    )
    st.markdown("")

question_text = st.text_input("Question:")

# Dynamically add or remove table column fields
for i in range(st.session_state.fields_size):
    col1, col2 = st.columns(2)
    with col1:
        field_value = st.text_input(f"Table column {i}", key=f"text{i}")
        st.session_state.fields[i] = field_value
    with col2:
        st.session_state.deletes.append(st.button("❌", key=f"delete{i}", on_click=delete_field, args=(i,)))
st.button("➕ Add table column name", on_click=add_field)

st.divider()

# Button to trigger translation
if st.button("Translate to SQL"):
    if question_text:
        input_data = make_input_string(question=question_text, table=st.session_state.fields)
        translate_and_show_result(input_data)
    else:
        st.warning("Please enter at least the question.")