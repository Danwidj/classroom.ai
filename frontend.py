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

# Initialize session state variables if they don't exist.
if "page" not in st.session_state:
    st.session_state["page"] = "generator"
if "quiz_data" not in st.session_state:
    st.session_state["quiz_data"] = []
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = {}

# final results view
if st.session_state["page"] == "final":
    st.title("Quiz Results")
    if not st.session_state.quiz_data:
        st.error("No quiz data available. Please generate a quiz first.")
    else:
        quiz_data = st.session_state.quiz_data
        user_answers = st.session_state.user_answers
        score = 0
        i = 0
        for quiz in quiz_data:
            st.subheader(f"Question {i+1}")
            st.write(f"**Question:** {quiz['question']}")
            options = quiz.get("options", {})
            for key, value in options.items():
                st.write(f"{key}: {value}")
            correct = quiz["correct"]
            user_answer = user_answers.get(i, None)
            if user_answer == correct:
                st.success(f"Your answer: {user_answer} (Correct)")
                score += 1
            else:
                st.error(f"Your answer: {user_answer} (Incorrect) — Correct answer: {correct}")
            st.write(f"Explanation: {quiz['explanation']}")
            st.markdown("---")
            i += 1
        st.write(f"**Your Score: {score} out of {len(quiz_data)}**")
    if st.button("Restart"):
        st.session_state["page"] = "generator"
        st.session_state["quiz_data"] = []
        st.session_state["user_answers"] = {}
        st.rerun()


# interactive quiz view
elif st.session_state["page"] == "quiz":
    st.title("Take the Quiz")
    if not st.session_state.quiz_data:
        st.error("No quiz data available. Please generate a quiz first.")
    else:
        quiz_data = st.session_state.quiz_data
        i = 0
        for quiz in quiz_data:
            st.subheader(f"Question {i+1}")
            st.write(quiz["question"])
            options = quiz.get("options", {})
            answer = st.radio(
                f"Select your answer for question {i+1}:",
                options=list(options.keys()),
                key=f"q{i}"
            )
            st.session_state.user_answers[i] = answer
            i += 1

        if st.button("Submit Answers"):
            st.session_state["page"] = "final"
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