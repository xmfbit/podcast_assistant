import openai

class ChatGPTSession(object):
    def __init__(self, system_msg: str):
        self.system_msg = system_msg
        self.reset()
    
    def _init_message(self):
        self.messages = [{'role': 'system', 'content': self.system_msg}]
    
    def reset(self):
        self._init_message()
    
    def chat(self, prompt):
        self.messages.append({'role': 'user', 'content': prompt})
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=self.messages)
        resp_text = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": resp_text})
        return resp_text
