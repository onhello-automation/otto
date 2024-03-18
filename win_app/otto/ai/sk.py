# TODO Generalize into an interface.

import semantic_kernel as sk
from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import \
	OllamaTextPromptExecutionSettings
from semantic_kernel.connectors.ai.ollama.services.ollama_text_completion import \
	OllamaTextCompletion
from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import \
	OllamaTextEmbedding
from semantic_kernel.connectors.memory.qdrant import QdrantMemoryStore
from semantic_kernel.functions import FunctionResult

COLLECTION_NAME = 'default'

from semantic_kernel.contents import TextContent

MEMORIES = [
	"I like vegan ice cream and pizza.",
	"I like to ski and bike.",
	"I like to watch sci-fi movies.",
]

QUESTION = "Tell me what I should do this weekend."

# See examples at
# https://github.com/microsoft/semantic-kernel/blob/main/python/tests/unit/connectors/ollama/services/test_ollama_chat_completion.py
# 

# Need patch for OllamaTextEmbedding.generate_embeddings:
'''
        result = []
        for text in texts:
            async with AsyncSession(self.session) as session:
                async with session.post(
                    self.url,
                    json={"model": self.ai_model_id, "prompt": text, "options": kwargs},
                ) as response:
                    response.raise_for_status()
                    response = await response.json()
                    result.append(response['embedding'])
        return array(result)
'''

async def main():
	# TODO Get from config.
	model = 'phi'
	# nomic-embed-text: size: 768
	# embedding_model = 'nomic-embed-text'
	# all-minilm: size: 384
	embedding_model = 'all-minilm'
	kernel = sk.Kernel()

	text_service = OllamaTextCompletion(ai_model_id=model, service_id='ollama_text_completion')
	kernel.add_service(text_service)

	embedding_service = OllamaTextEmbedding(ai_model_id=embedding_model, service_id='ollama_text_embedding')
	kernel.add_service(embedding_service)

	'''
	print(MEMORIES)
	e = await embedding_service.generate_embeddings(MEMORIES)
	print(e.shape)
	print(e)
	'''

	prompt = """
Tell the user what they should do.

User: {{$input}}
""".strip()

	settings = OllamaTextPromptExecutionSettings(ai_model_id=model, service_id=None)
	command = kernel.create_function_from_prompt('otto', 'otto', "Tell user what to do.", prompt, prompt_execution_settings=settings)

	arguments = sk.KernelArguments(input=QUESTION)
	invocation_response = await kernel.invoke(command, arguments=arguments)
	# print(invocation_response)
	assert isinstance(invocation_response, FunctionResult)
	response = invocation_response.value[0]
	assert isinstance(response, TextContent)
	assert response.inner_content is not None
	print(response.inner_content)
	print(type(response.inner_content))
	print(response.inner_content['response'])
	

	# Create a memory store.
	# store = QdrantMemoryStore()

if __name__ == "__main__":
	import asyncio
	asyncio.run(main())