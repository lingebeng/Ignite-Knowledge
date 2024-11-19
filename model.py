from openai import OpenAI

class Model:
    def __init__(self,api_key,role="You are a great knowledge manager"):
        self.role = role
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/")

    def generate(self,prompt):
        messages=[
            {"role":"system","content":self.role},
            {"role":"user","content":prompt},
        ]
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            temperature=2,
            max_tokens=4096,
        )

        gen_text = response.choices[0].message.content

        return gen_text

    def analyze(self):
        pass

