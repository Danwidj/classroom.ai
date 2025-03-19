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

# Initialize our own "page" state if it doesn't exist.
if "page" not in st.session_state:
    st.session_state["page"] = "generator"

# Render view based on the session state variable.
if st.session_state["page"] == "quiz":
    # Quiz display view
    st.title("Generated Quizzes")
    if "quiz_data" not in st.session_state or not st.session_state.quiz_data:
        st.error("No quiz data available. Please generate a quiz first.")
    else:
        quiz_data = st.session_state.quiz_data
        st.subheader("Your Quiz Questions:")
        for quiz in quiz_data:
            st.write(f"**Question:** {quiz['question']}")
            options = quiz.get("options", {})
            for key, value in options.items():
                st.write(f"{key}: {value}")
            st.info(f"Correct answer: {quiz['correct']}")
            st.write(f"Explanation: {quiz['explanation']}")
            st.markdown("---")
    
    if st.button("Go Back"):
        st.session_state["page"] = "generator"
        st.rerun()
        
else:
    # Quiz generation view
    st.title("Quiz Generator")
    prompt = st.text_input("Enter the quiz prompt", "quiz me about digital transformation")
    num_quizzes = st.number_input("Number of questions", min_value=1, max_value=10, value=3, step=1)
    
    if st.button("Generate Quiz"):
        if prompt and num_quizzes:
            quiz_data = get_quiz_data(prompt, num_quizzes)
            if quiz_data:
                st.session_state.quiz_data = quiz_data
                st.session_state["page"] = "quiz"
                st.rerun()
            else:
                st.error("Error generating quizzes. Please check the backend.")
        else:
            st.error("Please provide both a prompt and a number of quizzes.")