import streamlit as st
import requests

OPENAI_API_KEY = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/engines/text-davinci-002/completions'


def main():
    st.title("Essay Grader")

    prompt = st.text_area("Enter the prompt:")
    example_answer = st.text_area("Enter the example answer:")

    if st.button("Analyze"):
        feedback = analyze_answer(prompt, example_answer)
        st.write(feedback)

def analyze_answer(prompt, example_answer):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
    'prompt': f'{prompt}\n\nExample Answer: {example_answer}',
    'max_tokens': 3950,  # Adjusted to accommodate the length of the prompt
    'temperature': 0.7,
    'n': 1,
    'stop': None,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        st.write(response_data)  # For debugging, remove this line once the issue is resolved

        generated_feedback = response_data['choices'][0]['text'].strip()
        grade = perform_grading(generated_feedback)
        
        feedback = f"Generated Feedback: {generated_feedback}\nGrade: {grade}"
        return feedback
    else:
        st.write(f"Error: {response.status_code}, {response.text}")  # Print the error code and message
        return "Error in API request"

def perform_grading(generated_feedback):
    # Implement your grading logic here
    grade = 'A'  # Replace with your grading logic
    return grade

if __name__ == '__main__':
    main()
