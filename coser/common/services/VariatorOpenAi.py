from typing import List
from openai import OpenAI

class VariatiorOAI():

    def __init__(self,open_ai_key,prompt) -> None:
        self.key=open_ai_key
        self.prompt=prompt
        self.client = OpenAI(api_key=open_ai_key)
        pass


    def variate_prompts(self,prompts:List[str]):

        response = self.client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": self.prompt.format("\n-".join(prompts))},

        ]
        )
        return response
