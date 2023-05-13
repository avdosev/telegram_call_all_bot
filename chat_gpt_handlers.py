import openai

openai.api_key_path = "sensitive_info/openai_api_key.txt"

def get_answer(query, context=[]):
    model_engine = "gpt-3.5-turbo"
    completion = openai.ChatCompletion.create(
        model=model_engine, 
        messages=[
            *context,
            {"role": "user", "content": query}
        ],
        n=1)
    message = completion.choices[0].message.content
    return message


def simple_context(text, role='assistant'):
    return [{'role': role, 'content': text}]