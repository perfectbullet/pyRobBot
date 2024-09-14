"""Utils for using the OpenAI API."""

import hashlib
import shutil
from typing import TYPE_CHECKING, Optional

import openai
from loguru import logger

from . import GeneralDefinitions
from .chat_configs import OpenAiApiCallOptions
from .general_utils import retry
from .tokens import get_n_tokens_from_msgs

if TYPE_CHECKING:
    from .chat import Chat


class OpenAiClientWrapper(openai.OpenAI):
    """Wrapper for OpenAI API client."""

    def __init__(self, *args, private_mode: bool = False, **kwargs):
        """Initialize the OpenAI API client wrapper."""
        base_url = 'http://125.69.16.175:11434/v1'
        api_key = 'ollama'  # required, but unused
        kwargs['base_url'] = base_url
        kwargs['api_key'] = api_key
        super().__init__(**kwargs)
        self.private_mode = private_mode

        self.required_cache_files = [
            "chat_token_usage.db",
            "configs.json",
            "embeddings.db",
            "metadata.json",
        ]
        self.clear_invalid_cache_dirs()

    @property
    def cache_dir(self):
        """Return client's cache dir according to the privacy configs."""
        return self.get_cache_dir(private_mode=self.private_mode)

    @property
    def saved_chat_cache_paths(self):
        """Get the filepaths of saved chat contexts, sorted by last modified."""
        yield from sorted(
            (direc for direc in self.cache_dir.glob("chat_*/")),
            key=lambda fpath: fpath.stat().st_ctime,
        )

    def clear_invalid_cache_dirs(self):
        """Remove cache directories that are missing required files."""
        for directory in self.cache_dir.glob("chat_*/"):
            if not all(
                (directory / fname).exists() for fname in self.required_cache_files
            ):
                logger.debug(f"Removing invalid cache directory: {directory}")
                shutil.rmtree(directory, ignore_errors=True)

    def get_cache_dir(self, private_mode: Optional[bool] = None):
        """Return the directory where the chats using the client will be stored."""
        if private_mode is None:
            private_mode = self.private_mode

        if private_mode:
            client_id = "demo"
            parent_dir = GeneralDefinitions.PACKAGE_TMPDIR
        else:
            client_id = hashlib.sha256(self.api_key.encode("utf-8")).hexdigest()
            parent_dir = GeneralDefinitions.PACKAGE_CACHE_DIRECTORY

        directory = parent_dir / f"user_{client_id}"
        directory.mkdir(parents=True, exist_ok=True)

        return directory


def make_api_chat_completion_call(conversation: list, chat_obj: "Chat"):
    """Stream a chat completion from OpenAI API given a conversation and a chat object.

    Args:
        conversation (list): A list of messages passed as input for the completion.
        chat_obj (Chat): Chat object containing the configurations for the chat.

    Yields:
        str: Chunks of text generated by the API in response to the conversation.
    """
    api_call_args = {}
    for field in OpenAiApiCallOptions.model_fields:
        if getattr(chat_obj, field) is not None:
            api_call_args[field] = getattr(chat_obj, field)

    logger.trace(
        "Making OpenAI API call with chat=<{}>, args {} and messages {}",
        chat_obj.id,
        api_call_args,
        conversation,
    )

    logger.info('conversation is {}, api_call_args is {}'.format(conversation, api_call_args))

    @retry(max_n_attempts=2, error_msg="Problems connecting to OpenAI API")
    def stream_reply(conversation, **api_call_args):
        # Update the chat's token usage database with tokens used in chat input
        # Do this here because every attempt consumes tokens, even if it fails
        n_tokens = get_n_tokens_from_msgs(messages=conversation, model=chat_obj.model)
        for db in [chat_obj.general_token_usage_db, chat_obj.token_usage_db]:
            db.insert_data(model=chat_obj.model, n_input_tokens=n_tokens)

        full_reply_content = ""
        for completion_chunk in chat_obj.openai_client.chat.completions.create(
            messages=conversation, stream=True, **api_call_args
        ):
            reply_chunk = getattr(completion_chunk.choices[0].delta, "content", "")
            if reply_chunk is None:
                break
            full_reply_content += reply_chunk
            yield reply_chunk

        # Update the chat's token usage database with tokens used in chat output
        reply_as_msg = {"role": "assistant", "content": full_reply_content}
        n_tokens = get_n_tokens_from_msgs(messages=[reply_as_msg], model=chat_obj.model)
        for db in [chat_obj.general_token_usage_db, chat_obj.token_usage_db]:
            db.insert_data(model=chat_obj.model, n_output_tokens=n_tokens)

    logger.trace("Done with OpenAI API call")
    yield from stream_reply(conversation, **api_call_args)
