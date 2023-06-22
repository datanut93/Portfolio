
import streamlit as st
import requests

OPENAI_API_KEY = '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'
OPENAI_API_URL = 'https://api.openai.com/v1/engines/text-davinci-003/completions'


def main():
    st.title("Recipe App")

    ingredients = st.text_area("Enter the ingredients you have in your kitchen (separated by commas):")

    if st.button("Find Recipes"):
        recipes = find_recipes(ingredients)
        st.write(recipes)


def find_recipes(ingredients):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENAI_API_KEY}'
    }

    data = {
        'prompt': f'I have the following ingredients in my kitchen: {ingredients}\n\nWhat are some possible recipes I can make with these ingredients?',
        'max_tokens': 1000,
        'temperature': 0.7,
        'n': 3,
        'stop': None,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        recipes = [choice['text'].strip() for choice in response_data['choices']]
        return recipes
    else:
        return f"Error: {response.status_code}, {response.json()}"


if __name__ == '__main__':
    main()
