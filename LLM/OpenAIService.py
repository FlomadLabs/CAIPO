import openai


from LLM.LLMService import LLMService


class OpenAIService(LLMService):
    def query(self, prompt, api_key, model_name):
        response = openai.Completion.create(
            engine=model_name,
            prompt=prompt,
            max_tokens=4096,
            api_key=api_key
        )
        return response.choices[0].text.strip() if response.choices else None