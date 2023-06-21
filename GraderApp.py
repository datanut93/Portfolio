import streamlit as st
import openai

# Set up your OpenAI API credentials
openai.api_key = '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'

# Define your Streamlit app layout
def main():
    st.title("Essay Grader")
    
    # User input: Prompt
    prompt = st.text_area("Enter the prompt:")
    
    # User input: Example answer
    example_answer = st.text_area("Enter the example answer:")
    
    # Analyze and provide feedback
    if st.button("Analyze"):
        feedback = analyze_answer(prompt, example_answer)
        st.write(feedback)
        
# Function to analyze the answer and provide feedback
def analyze_answer(prompt, example_answer):
    # Generate response using Chat GPT
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt + "\n\nExample Answer: " + example_answer,
        max_tokens=100,
        temperature=0.7,
        n=1,
        stop=None,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # Get the generated feedback
    generated_feedback = response.choices[0].text.strip()
    
    # Perform grading and provide feedback
    grade = perform_grading(generated_feedback)  # Implement your grading logic here
    feedback = f"Generated Feedback: {generated_feedback}\nGrade: {grade}"
    
    return feedback

# Function to perform grading (replace with your grading logic)
def perform_grading(generated_feedback):
    # Implement your grading logic here
    # Assign a grade based on the analysis of the generated feedback
    grade = 'A'  # Replace with your grading logic
    
    return grade

if __name__ == '__main__':
    main()
