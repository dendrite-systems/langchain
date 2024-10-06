from __future__ import annotations

from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class DownloadInput(BaseModel):
    """Input for Download."""

    download_path: str = Field(
        ...,
        description="The path to download the file to.",
    )


class Download(BaseDendriteTool):
    """Download a file from the page."""

    name: str = "download_file_with_browser"
    description: str = (
        "Downloads a file from the page to the specified path. Assumes that some download is already happening."
    )
    args_schema: Type[BaseModel] = DownloadInput

    def _run(
        self,
        download_path: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            pw_page = self.client.get_active_page().playwright_page
            download = self.client._get_download(pw_page)
            download.save_as(download_path)
            return f"File successfully downloaded to {download_path}"
        except Exception as e:
            return f"Error occurred when getting download, exception: {e}"

    async def _arun(
        self,
        download_path: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            page = await self.async_client.get_active_page()
            pw_page = page.playwright_page
            download = await self.async_client._get_download(pw_page)
            await download.save_as(download_path)
            return f"File successfully downloaded to {download_path}"
        except Exception as e:
            return f"Error occurred when getting download, exception: {e}"
