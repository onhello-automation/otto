import asyncio
import logging
import sys
from dataclasses import dataclass, field
from logging import Logger

import semantic_kernel as sk
from injector import inject
from semantic_kernel.connectors.ai.ollama.services.ollama_text_completion import \
    OllamaTextCompletion
from semantic_kernel.connectors.ai.ollama.services.ollama_text_embedding import \
    OllamaTextEmbedding
from semantic_kernel.contents import StreamingTextContent
from semantic_kernel.core_plugins.text_memory_plugin import TextMemoryPlugin
from semantic_kernel.memory.semantic_text_memory import SemanticTextMemory
from tqdm import tqdm

from otto.ai.commander import Commander
from otto.ai.sk.sk_config import SKConfig
from otto.command import Command
from otto.context.window import WindowInfo

# See examples at
# https://github.com/microsoft/semantic-kernel/blob/main/python/tests/unit/connectors/ollama/services/test_ollama_chat_completion.py


@inject
@dataclass
class SemanticKernelAdapter(Commander):
    _logger: Logger
    _sk_config: SKConfig

    _fact_collection_name: str = field(default='facts', init=False)
    _kernel: sk.Kernel = field(init=False)
    _sk_function: sk.KernelFunction = field(init=False)

    def __post_init__(self):
        self._logger.info("Initializing kernel and memory.")
        kernel = sk.Kernel()

        service_id = 'ollama_text_completion'
        ai_model = self._sk_config.ai_model
        text_service = OllamaTextCompletion(ai_model_id=ai_model, service_id=service_id)
        kernel.add_service(text_service)

        embedding_model = self._sk_config.embedding_model
        embedding_service = OllamaTextEmbedding(ai_model_id=embedding_model, service_id='ollama_text_embedding')
        kernel.add_service(embedding_service)

        # Following https://github.com/microsoft/semantic-kernel/blob/main/python/notebooks/06-memory-and-embeddings.ipynb
        memory = SemanticTextMemory(storage=sk.memory.VolatileMemoryStore(), embeddings_generator=embedding_service)
        memory_plugin = TextMemoryPlugin(memory)
        kernel.import_plugin_from_object(memory_plugin, "TextMemoryPlugin")

        knowledge = self._sk_config.knowledge

        self._logger.debug("Saving knowledge.")
        for i, fact in enumerate(tqdm(knowledge,
                                      desc="Saving knowledge",
                                      unit="fact",
                                      )):
            asyncio.run(memory.save_information(self._fact_collection_name, fact, id=str(i)))

        prompt = self._sk_config.prompt
        self._logger.debug("Prompt:\n\"%s\"", prompt)
        self._sk_function = kernel.create_function_from_prompt('otto', 'otto', "Tell user what to do.", prompt)
        self._kernel = kernel

    async def get_command(self, active_window: WindowInfo) -> Command:
        """
        Get a command to tell the user based on the active window.
        """
        # TODO Pass text from the active window as context.
        # TODO Stream the text back.
        arguments = sk.KernelArguments(
            active_window_process_name=active_window.process_name,
            active_window_title=active_window.title,
            fact_collection=self._fact_collection_name,
        )
        arguments[TextMemoryPlugin.RELEVANCE_PARAM] = 0.5
        self._logger.info("Invoking kernel. Response:")
        is_logging_enabled = self._logger.isEnabledFor(logging.INFO)
        command_text = ""
        async for results in self._kernel.invoke_stream(self._sk_function, arguments=arguments):
            for r in results:
                assert isinstance(r, StreamingTextContent)
                if r.text:
                    if is_logging_enabled:
                        print(r.text, end="")
                        sys.stdout.flush()
                    command_text += r.text
        if is_logging_enabled:
            print()

        return Command(command_text)
