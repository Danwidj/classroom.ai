import streamlit as st

st.title("Generated Quizzes")

# Check if quiz data is available in session state
if "quiz_data" not in st.session_state or not st.session_state.quiz_data:
    st.error("No quiz data available. Please generate a quiz first.")
    st.stop()

quiz_data = st.session_state.quiz_data

st.subheader("Your Quiz Questions:")
for quiz in quiz_data:
    st.write(f"**Quiz:** {quiz}")
