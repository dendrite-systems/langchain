from __future__ import annotations

import json
import threading
from typing import Any, Optional, Type, Union

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class ExtractInput(BaseModel):
    """Input for Extract."""

    prompt: str = Field(
        ...,
        description="The prompt to guide the extraction from the current page.",
    )
    type_spec: Optional[str] = Field(
        None,
        description="The type specification for the extracted data. Can be 'str', 'int', 'float', 'bool', or a JSON schema string.",
    )


class Extract(BaseDendriteTool):
    """Extract data from the current page."""

    name: str = "extract_from_page_with_browser"
    description: str = (
        "Extracts data by looking at the current page's HTML, based on a prompt and optional type specification. More expensive and slow than the ask tool, but can extract more complex data."
    )
    args_schema: Type[BaseModel] = ExtractInput

    def _run(
        self,
        prompt: str,
        type_spec: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            type_spec_obj = self._get_type_spec(type_spec)
            res = self.client.extract(prompt, type_spec=type_spec_obj)
        except Exception as e:
            return f"Error occurred when extracting from page, exception: {e}"

        return f"Extracted data from page: {res}"

    async def _arun(
        self,
        prompt: str,
        type_spec: Optional[str] = None,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            type_spec_obj = self._get_type_spec(type_spec)
            res = await self.async_client.extract(prompt, type_spec=type_spec_obj)
        except Exception as e:
            return f"Error occurred when extracting from page, exception: {e}"

        return f"Extracted data from page: {res}"

    @staticmethod
    def _get_type_spec(type_spec: Optional[str]) -> Optional[Union[Type, dict]]:
        """Convert string type_spec to actual type or JSON schema."""
        if type_spec is None:
            return None

        type_map = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        }

        lower_type_spec = type_spec.lower()
        if lower_type_spec in type_map:
            return type_map[lower_type_spec]

        try:
            # Attempt to parse as JSON schema
            return json.loads(type_spec)
        except json.JSONDecodeError:
            raise ValueError(
                f"Invalid type_spec: {type_spec}. Must be 'str', 'int', 'float', 'bool', or a valid JSON schema string."
            )
