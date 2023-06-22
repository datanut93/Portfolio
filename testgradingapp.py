import streamlit as st
import requests

OPENAI_API_KEY = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/engines/text-davinci-003/completions'


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
        'prompt': f'{prompt}\n\nExample Answer: {example_answer}\n\nYou are acting as my personal tutor. My goal is to judge how well I have written an essay based off of a prompt. I have provided my answer which I want you to grade based off the provided prompt and grading criteria. Ensuring my adherance to the prompt and make sure I answer all parts of the question to give me a grade on a scale of 1-100:',
        'max_tokens': 1000,
        'temperature': 0.7,
        'n': 1,
        'stop': None,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        generated_feedback = response_data['choices'][0]['text'].strip()
        return generated_feedback
    else:
        return f"Error: {response.status_code}, {response.json()}"


def perform_grading(generated_feedback):
    # Implement your grading logic here
    grade = 'A'  # Replace with your grading logic
    return grade

if __name__ == '__main__':
    main()
