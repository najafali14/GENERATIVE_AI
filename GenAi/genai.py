import google.generativeai as genai
import os
import streamlit as st

from dotenv import load_dotenv
import google.ai.generativelanguage as glm
# Load environment variables from .env file
load_dotenv()
# Access environment variables
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)


st.header('GenAi Smart Calculator')
calculator = glm.Tool(
    function_declarations=[
      glm.FunctionDeclaration(
        name='multiply',
        description="Returns the product of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a':glm.Schema(type=glm.Type.NUMBER),
                'b':glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      ),
      glm.FunctionDeclaration(
        name='addition',
        description="Returns the addition of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a':glm.Schema(type=glm.Type.NUMBER),
                'b':glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      ),
      glm.FunctionDeclaration(
        name='subtract',
        description="Returns the subtraction of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a':glm.Schema(type=glm.Type.NUMBER),
                'b':glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      ),
      glm.FunctionDeclaration(
        name='division',
        description="Returns the division of two numbers.",
        parameters=glm.Schema(
            type=glm.Type.OBJECT,
            properties={
                'a':glm.Schema(type=glm.Type.NUMBER),
                'b':glm.Schema(type=glm.Type.NUMBER)
            },
            required=['a','b']
        )
      ),
    ])

calculator = {'function_declarations': [
      {'name': 'multiply',
       'description': 'Returns the product of two numbers.',
       'parameters': {'type_': 'OBJECT',
       'properties': {
         'a': {'type_': 'NUMBER'},
         'b': {'type_': 'NUMBER'} },
       'required': ['a', 'b']} },
       {'name': 'addition',
       'description': 'Returns the addition of two numbers.',
       'parameters': {'type_': 'OBJECT',
       'properties': {
         'a': {'type_': 'NUMBER'},
         'b': {'type_': 'NUMBER'} },
       'required': ['a', 'b']} },
       {'name': 'subtract',
       'description': 'Returns the subtraction of two numbers.',
       'parameters': {'type_': 'OBJECT',
       'properties': {
         'a': {'type_': 'NUMBER'},
         'b': {'type_': 'NUMBER'} },
       'required': ['a', 'b']} },
       {'name': 'division',
       'description': 'Returns the division of two numbers.',
       'parameters': {'type_': 'OBJECT',
       'properties': {
         'a': {'type_': 'NUMBER'},
         'b': {'type_': 'NUMBER'} },
       'required': ['a', 'b']} },
       ]}

glm.Tool(calculator)
model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                              tools=[calculator])
user_inp = st.chat_input('Enter prompt...')

if user_inp:
    # Start chat with generative model
    chat = model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(user_inp)

    # Parse function call from response
    fc = response.candidates[0].content.parts[0].function_call
    assert fc.name in ['multiply', 'addition', 'subtract', 'division']

    # Perform operation based on function call
    if fc.name == 'multiply':
        result = fc.args['a'] * fc.args['b']
    elif fc.name == 'addition':
        result = fc.args['a'] + fc.args['b']
    elif fc.name == 'subtract':
        result = fc.args['a'] - fc.args['b']
    elif fc.name == 'division':
        result = fc.args['a'] / fc.args['b']
    else:
        result = 'Invalid operation'

    st.write('You: ',user_inp)

    st.write('Bot: ',result)
else:
    st.write('Smart Calculator Created by Najaf Ali')