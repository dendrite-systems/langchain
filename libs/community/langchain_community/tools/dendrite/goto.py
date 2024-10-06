from __future__ import annotations

import threading
from typing import Optional, Type
from urllib.parse import urlparse

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field, model_validator

from langchain_community.tools.dendrite.base import BaseDendriteTool

from dendrite_sdk._common._exceptions.dendrite_exception import IncorrectOutcomeError


class GotoInput(BaseModel):
    """Input for GotoInput."""

    url: str = Field(..., description="url to navigate to")
    # expected_page: Optional[str] = Field(
    #     None,
    #     description="the expected page described in natural language, e.g 'the dashboard'",
    # )

    @model_validator(mode="before")
    @classmethod
    def validate_url_scheme(cls, values: dict) -> dict:
        """Check that the URL scheme is valid."""
        url = values.get("url")
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ("http", "https"):
            raise ValueError("URL scheme must be 'http' or 'https'")
        return values


class Goto(BaseDendriteTool):
    """Tool for navigating a browser to a URL.

    **Security Note**: This tool provides code to control web-browser navigation.

        This tool can navigate to any URL, including internal network URLs, and
        URLs exposed on the server itself.

        However, if exposing this tool to end-users, consider limiting network
        access to the server that hosts the agent.

        By default, the URL scheme has been limited to 'http' and 'https' to
        prevent navigation to local file system URLs (or other schemes).

        If access to the local file system is required, consider creating a custom
        tool or providing a custom args_schema that allows the desired URL schemes.

        See https://python.langchain.com/docs/security for more information.
    """

    name: str = "goto_with_browser"
    description: str = "Navigate with the Dendrite browser to a given URL."
    args_schema: Type[BaseModel] = GotoInput

    def _run(
        self,
        url: str,
        # expected_page: str = "",
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            self.client.goto(url)
        except IncorrectOutcomeError as e:
            return f"Unexpected navigation to {url}, reason: {e}\n\nRemember: If unauthenticated, certain navigation may be restricted. Remind the user to initialize the Dendrite Client with the correct auth params if this seems to be the case."
        except Exception as e:
            return f"Error navigating to {url}, exception: {e}"

        return f"Successfully navigated to {url}."

    async def _arun(
        self,
        url: str,
        # expected_page: str = "",
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            await self.async_client.goto(url)
        except IncorrectOutcomeError as e:
            return f"Unexpected navigation to {url}, reason: {e}\n\nRemember: If unauthenticated, certain navigation may be restricted. Remind the user to initialize the Dendrite Client with the correct auth params if this seems to be the case."
        except Exception as e:
            return f"Error navigating to {url}, exception: {e}"

        return f"Successfully navigated to {url}."
