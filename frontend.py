import streamlit as st
import requests
import json

# Function to make the POST request to the backend
def get_quiz_data(prompt, num_quizzes):
    url = "http://127.0.0.1:5000/generate-quiz"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "num_quizzes": num_quizzes  
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Streamlit UI setup
st.title("Quiz Generator")

# Input fields for user to provide prompt and number of quizzes
prompt = st.text_input("Enter the quiz prompt", "quiz me about digital transformation")
num_quizzes = st.number_input("Number of questions", min_value=1, max_value=10, value=3, step=1)

# Button to trigger the quiz generation
if st.button("Generate Quiz"):
    if prompt and num_quizzes:
        quiz_data = get_quiz_data(prompt, num_quizzes)
        if quiz_data:
            # Store quiz data in session state for use in the quiz page
            st.session_state.quiz_data = quiz_data
            # Redirect to the quiz page using st.set_query_params
            st.st.query_params(page="quiz")
            st.experimental_rerun()
        else:
            st.error("Error generating quizzes. Please check the backend.")
    else:
        st.error("Please provide both a prompt and a number of quizzes.")