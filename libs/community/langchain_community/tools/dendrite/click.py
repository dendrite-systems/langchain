from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class ClickInput(BaseModel):
    """Input for Click."""

    prompt: str = Field(
        ...,
        description="The prompt describing the element to be clicked.",
    )
    # expected_outcome: Optional[str] = Field(
    #     None,
    #     description="The expected outcome of the click action. e.g 'we are redirected to the dashboard'",
    # )


class Click(BaseDendriteTool):
    """Click an element on the page."""

    name: str = "click_element_with_browser"
    description: str = "Clicks an element on the page based on the provided prompt."
    args_schema: Type[BaseModel] = ClickInput

    def _run(
        self,
        prompt: str,
        # expected_outcome: Optional[str] = None,
        use_cache: bool = True,
        timeout: int = 15000,
        force: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            res = self.client.click(
                prompt,
                # expected_outcome=expected_outcome,
                use_cache=use_cache,
                timeout=timeout,
                force=force,
            )
            return f"Click action performed: {res}"
        except Exception as e:
            return f"Error occurred when clicking element, exception: {e}"

    async def _arun(
        self,
        prompt: str,
        # expected_outcome: Optional[str] = None,
        use_cache: bool = True,
        timeout: int = 15000,
        force: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            res = await self.async_client.click(
                prompt,
                # expected_outcome=expected_outcome,
                use_cache=use_cache,
                timeout=timeout,
                force=force,
            )
            return f"Click action performed: {res}"
        except Exception as e:
            return f"Error occurred when clicking element, exception: {e}"
