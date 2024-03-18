import semantic_kernel as sk
from semantic_kernel.connectors.ai.ollama.ollama_prompt_execution_settings import \
	OllamaTextPromptExecutionSettings
from semantic_kernel.connectors.ai.ollama.services.ollama_text_completion import \
	OllamaTextCompletion
from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import \
	OllamaTextEmbedding
from semantic_kernel.contents import TextContent
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.functions import FunctionResult
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory


COLLECTION_NAME = 'generic'


MEMORIES = [
	"I like vegan ice cream and pizza.",
	"I like to ski and bike.",
	"I like to watch sci-fi movies.",
]

QUESTION = "Tell me what sports I should do this weekend based on what I like to do."

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

# Need patch for OllamaTextCompletion.complete:
"""
                response.raise_for_status()
                inner_content = await response.json()
                text = inner_content['response']
                return [TextContent(inner_content=inner_content, ai_model_id=self.ai_model_id, text=text)]
"""


async def main():
	# TODO Get from config.
	model = 'phi'
	# nomic-embed-text: size: 768
	embedding_model = 'nomic-embed-text'
	# all-minilm: size: 384
	# vector_size = 384
	# embedding_model = 'all-minilm'
	kernel = sk.Kernel()

	service_id = 'ollama_text_completion'
	text_service = OllamaTextCompletion(ai_model_id=model, service_id=service_id)
	kernel.add_service(text_service)

	embedding_service = OllamaTextEmbedding(ai_model_id=embedding_model, service_id='ollama_text_embedding')
	kernel.add_service(embedding_service)

	'''
	print(MEMORIES)
	e = await embedding_service.generate_embeddings(MEMORIES)
	print(e.shape)
	print(e)
	'''

	# Following https://github.com/microsoft/semantic-kernel/blob/main/python/notebooks/06-memory-and-embeddings.ipynb
	memory = SemanticTextMemory(storage=sk.memory.VolatileMemoryStore(), embeddings_generator=embedding_service)
	memory_plugin = TextMemoryPlugin(memory)
	kernel.import_plugin_from_object(memory_plugin, "TextMemoryPlugin")

	print("Saving memories.")
	for i, mem in enumerate(MEMORIES):
		await memory.save_information(COLLECTION_NAME, mem, id=str(i))

	print("Searching memory.")
	result = await memory.search(COLLECTION_NAME, QUESTION)
	for r in result:
		print(r.relevance, r.text)

	prompt = """
Tell the user what they should do.

Context: {{recall $input}}

User: {{$input}}
""".strip()

	settings = OllamaTextPromptExecutionSettings(ai_model_id=model, service_id=service_id)
	command = kernel.create_function_from_prompt('otto', 'otto', "Tell user what to do.", prompt, prompt_execution_settings=settings)

	arguments = sk.KernelArguments(input=QUESTION)
	arguments[TextMemoryPlugin.RELEVANCE_PARAM] = 0.5

	print("Invoking kernel.")
	invocation_response = await kernel.invoke(command, arguments=arguments)
	assert isinstance(invocation_response, FunctionResult)
	response = invocation_response.value[0]
	assert isinstance(response, TextContent)
	print(response.text)


if __name__ == "__main__":
	import asyncio
	asyncio.run(main())
