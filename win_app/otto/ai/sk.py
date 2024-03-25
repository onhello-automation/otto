import logging
import sys

import semantic_kernel as sk
from semantic_kernel.connectors.ai.ollama.services.ollama_text_completion import \
    OllamaTextCompletion
from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import \
    OllamaTextEmbedding
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from semantic_kernel.contents import StreamingTextContent


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


async def main():
    # TODO Get from config.
    model = 'phi'
    # nomic-embed-text: size: 768
    embedding_model = 'nomic-embed-text'
    # all-minilm: size: 384
    # vector_size = 384
    # embedding_model = 'all-minilm'
    kernel = sk.Kernel()
    logging.basicConfig(level=logging.DEBUG)

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
Tell the user what they should do in one or two short sentences.

Context: {{recall $input}}

User: {{$input}}
""".strip()

    command = kernel.create_function_from_prompt('otto', 'otto', "Tell user what to do.", prompt)

    arguments = sk.KernelArguments(input=QUESTION)
    arguments[TextMemoryPlugin.RELEVANCE_PARAM] = 0.5
    print("Invoking kernel. Response:")
    async for results in kernel.invoke_stream(command, arguments=arguments):
        for r in results:
            assert isinstance(r, StreamingTextContent)
            print(r.text, end="")
            sys.stdout.flush()
    print()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
