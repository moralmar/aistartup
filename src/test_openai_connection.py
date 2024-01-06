from openai import OpenAI
import os
from dotenv import load_dotenv


# take environment variables from .env.
load_dotenv()


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
print(completion.choices[0].message.content)
print(f'model: {completion.model}')
print(f'completion_tokens: {str(completion.usage.completion_tokens)}')
print(f'prompt_tokens: {str(completion.usage.prompt_tokens)}')
print(f'total_tokens: {str(completion.usage.total_tokens)}')
