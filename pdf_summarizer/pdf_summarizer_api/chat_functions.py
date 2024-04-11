from openai import OpenAI
from dotenv import load_dotenv 
import os
load_dotenv()

api_key = os.getenv('api_key')

client = OpenAI(api_key=api_key) 

def set_open_params(model = 'gpt-3.5-turbo-0125', temperature = 0.6, max_tokens = 256, top_p = 1, frequency_penalty = 0, presence_penalty =0,):
    openai_params = {}
    openai_params['model'] = model
    openai_params['temperature'] = temperature
    openai_params['max_tokens'] = max_tokens
    openai_params['top_p'] = top_p
    openai_params['frequency_penalty'] = frequency_penalty
    openai_params['presence_penalty'] = presence_penalty
    return openai_params

def get_completion(params, messages):
    response = client.chat.completions.create(
        model = params['model'],
        messages = messages,
        temperature = params['temperature'],
        max_tokens = params['max_tokens'],
        top_p = params['top_p'],
        frequency_penalty = params['frequency_penalty'],
        presence_penalty = params['presence_penalty'],
    )
    return response.choices[0].message.content
