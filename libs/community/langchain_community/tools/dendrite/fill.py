from __future__ import annotations

from typing import Optional, Type, Dict, Any

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class FillInput(BaseModel):
    """Input for Fill."""

    prompt: str = Field(
        ...,
        description="The prompt describing the element to be filled.",
    )
    value: str = Field(
        ...,
        description="The value to fill the element with.",
    )
    # expected_outcome: Optional[str] = Field(
    #     None,
    #     description="The expected outcome of the fill action.",
    # )


class Fill(BaseDendriteTool):
    """Fill an element on the page."""

    name: str = "fill_element_with_browser"
    description: str = (
        "Fills an element on the page based on the provided prompt and value."
    )
    args_schema: Type[BaseModel] = FillInput

    def _run(
        self,
        prompt: str,
        value: str,
        # expected_outcome: Optional[str] = None,
        use_cache: bool = True,
        timeout: int = 15000,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            res = self.client.fill(
                prompt,
                value,
                # expected_outcome=expected_outcome,
                use_cache=use_cache,
                timeout=timeout,
            )
            return f"Fill action performed: {res.message}"
        except Exception as e:
            return f"Error occurred when filling element, exception: {e}"

    async def _arun(
        self,
        prompt: str,
        value: str,
        # expected_outcome: Optional[str] = None,
        use_cache: bool = True,
        timeout: int = 15000,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            res = await self.async_client.fill(
                prompt,
                value,
                # expected_outcome=expected_outcome,
                use_cache=use_cache,
                timeout=timeout,
            )
            return f"Fill action performed: {res.message}"
        except Exception as e:
            return f"Error occurred when filling element, exception: {e}"


class FillFieldsInput(BaseModel):
    """Input for FillFields."""

    fields: Dict[str, Any] = Field(
        ...,
        description="A dictionary where each key is a field identifier and each value is the content to fill in that field.",
    )


class FillFields(BaseDendriteTool):
    """Fill multiple fields on the page."""

    name: str = "fill_multiple_fields_with_browser"
    description: str = (
        "Fills multiple fields on the page based on the provided dictionary of prompts and values. "
    )
    args_schema: Type[BaseModel] = FillFieldsInput

    def _run(
        self,
        fields: Dict[str, Any],
        use_cache: bool = True,
        timeout: int = 15000,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            results = []
            for field, value in fields.items():
                prompt = f"I'll be filling in several values from an object with these keys: {list(fields.keys())} in this page. Get the field best described as '{field}'. I want to fill it with a '{type(value)}' type value."
                res = self.client.fill(
                    prompt,
                    value,
                    use_cache=use_cache,
                    timeout=timeout,
                )
                results.append(f"Field '{field}': {res.message}")
            return f"Multiple fields filled: {'; '.join(results)}"
        except Exception as e:
            return f"Error occurred when filling multiple fields, exception: {e}"

    async def _arun(
        self,
        fields: Dict[str, Any],
        use_cache: bool = True,
        timeout: int = 15000,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            results = []
            for field, value in fields.items():
                prompt = f"I'll be filling in several values from an object with these keys: {list(fields.keys())} in this page. Get the field best described as '{field}'. I want to fill it with a '{type(value)}' type value."
                res = await self.async_client.fill(
                    prompt,
                    value,
                    use_cache=use_cache,
                    timeout=timeout,
                )
                results.append(f"Field '{field}': {res.message}")
            return f"Multiple fields filled."
        except Exception as e:
            return f"Error occurred when filling multiple fields, exception: {e}"
