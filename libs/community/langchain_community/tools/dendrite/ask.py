from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class LookAtPageInput(BaseModel):
    """Input for Ask."""

    prompt: str = Field(
        ...,
        description="What would you like to ask the page? E.g 'I'm trying to log in, please describe the page so I can fill out the form.'",
    )


class Ask(BaseDendriteTool):
    """Ask a question to the page."""

    name: str = "ask_page_with_browser"
    description: str = (
        "Looks at the current page and answers a question about it. Useful to describe the current page. Always use this when navigating to a new page so you can understand what you're looking at. This tool can also be used to return data small, visible data such as 'companies phone number'."
    )
    args_schema: Type[BaseModel] = LookAtPageInput

    def _run(
        self,
        prompt: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            res = self.client.ask(prompt, str)
        except Exception as e:
            return f"Error occured when asking page, exception: {e}"

        return f"Response from ask page: {res}"

    async def _arun(
        self,
        prompt: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            res = await self.async_client.ask(prompt, str)
        except Exception as e:
            return f"Error occurred when asking page, exception: {e}"

        return f"Reponse from ask page: {res}"
