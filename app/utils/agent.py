import ollama
from transformers import AutoTokenizer
# from vllm import LLM, SamplingParams
# pip install git+https://github.com/OpenBMB/vllm.git@minicpm3

class Agent:
    def __init__(self, system_prompt: str) -> None:
        OLLAMA_HOST = "http://localhost:11434"
        self.client = ollama.Client(host=OLLAMA_HOST)
        self.system_prompt = system_prompt

    async def chat(self, messages, model="qwen2:7b"):
        try:
            if messages[0]['role'] != 'system':
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    *messages
                ]
            response = self.client.chat(
                model=model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")

# class MiniCPM3Agent(Agent):
#     def __init__(self, system_prompt: str) -> None:
#         super().__init__(system_prompt)
#         self.model_name = "openbmb/MiniCPM3-4B"
#         self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
#         self.sampling_params = SamplingParams(top_p=0.7, temperature=0.7, max_tokens=1024)
#         self.llm = LLM(model=self.model_name,
#             trust_remote_code=True,
#             tensor_parallel_size=1
#         )

#     async def chat(self, messages, model="openbmb/MiniCPM3-4B"):
#         try:
#             if messages[0]['role'] != 'system':
#                 messages = [
#                     {"role": "system", "content": self.system_prompt},
#                     *messages
#                 ]
#             input_text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)   
#             outputs = self.llm.generate(prompts=input_text, sampling_params=self.sampling_params)
#             return outputs[0].outputs[0].text
#         except Exception as e:
#             raise Exception(f"Error generating response: {str(e)}")