from __future__ import annotations

from typing import Optional, Type, Union, Sequence, List
import pathlib

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class UploadInput(BaseModel):
    """Input for Upload."""

    files: Union[str, List[str]] = Field(
        ...,
        description="The file(s) to upload. Can be a single file path or a list of file paths.",
    )


class Upload(BaseDendriteTool):
    """Upload files to the page."""

    name: str = "upload_files_with_browser"
    description: str = "Uploads one or more files to the page using a file chooser."
    args_schema: Type[BaseModel] = UploadInput

    def _process_files_input(
        self, files: Union[str, List[str]]
    ) -> Sequence[Union[str, pathlib.Path]]:
        if isinstance(files, str):
            return [files]
        return files

    def _run(
        self,
        files: Union[str, List[str]],
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            page = self.client.get_active_page()
            processed_files = self._process_files_input(files)
            page.upload_files(processed_files)
            return f"File(s) successfully uploaded"
        except Exception as e:
            return f"Error occurred when uploading file(s), exception: {e}"

    async def _arun(
        self,
        files: Union[str, List[str]],
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            page = await self.async_client.get_active_page()
            processed_files = self._process_files_input(files)
            await page.upload_files(processed_files)
            return f"File(s) successfully uploaded"
        except Exception as e:
            return f"Error occurred when uploading file(s), exception: {e}"
