from __future__ import annotations

from typing import Optional, Type, Union, Literal

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from pydantic import BaseModel, Field

from langchain_community.tools.dendrite.base import BaseDendriteTool


class PressInput(BaseModel):
    """Input for Press."""

    key: Union[
        str,
        Literal[
            "Enter",
            "Tab",
            "Escape",
            "Backspace",
            "ArrowUp",
            "ArrowDown",
            "ArrowLeft",
            "ArrowRight",
        ],
    ] = Field(..., description="The main key to be pressed.")
    hold_shift: bool = Field(False, description="Whether to hold the Shift key.")
    hold_ctrl: bool = Field(False, description="Whether to hold the Control key.")
    hold_alt: bool = Field(False, description="Whether to hold the Alt key.")
    hold_cmd: bool = Field(
        False, description="Whether to hold the Command key (Meta on some systems)."
    )


class Press(BaseDendriteTool):
    """Press a keyboard key on the active page."""

    name: str = "press_key_with_browser"
    description: str = (
        "Presses a keyboard key on the active page, optionally with modifier keys."
    )
    args_schema: Type[BaseModel] = PressInput

    def _run(
        self,
        key: Union[
            str,
            Literal[
                "Enter",
                "Tab",
                "Escape",
                "Backspace",
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
            ],
        ],
        hold_shift: bool = False,
        hold_ctrl: bool = False,
        hold_alt: bool = False,
        hold_cmd: bool = False,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        if self.client is None:
            raise ValueError(f"Dendrite client not provided to {self.name}")

        try:
            self.client.press(
                key,
                hold_shift=hold_shift,
                hold_ctrl=hold_ctrl,
                hold_alt=hold_alt,
                hold_cmd=hold_cmd,
            )
            return f"Key press action performed: {key}"
        except Exception as e:
            return f"Error occurred when pressing key, exception: {e}"

    async def _arun(
        self,
        key: Union[
            str,
            Literal[
                "Enter",
                "Tab",
                "Escape",
                "Backspace",
                "ArrowUp",
                "ArrowDown",
                "ArrowLeft",
                "ArrowRight",
            ],
        ],
        hold_shift: bool = False,
        hold_ctrl: bool = False,
        hold_alt: bool = False,
        hold_cmd: bool = False,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        if self.async_client is None:
            raise ValueError(f"Async Dendrite client not provided to {self.name}")

        try:
            await self.async_client.press(
                key,
                hold_shift=hold_shift,
                hold_ctrl=hold_ctrl,
                hold_alt=hold_alt,
                hold_cmd=hold_cmd,
            )
            return f"Key press action performed: {key}"
        except Exception as e:
            return f"Error occurred when pressing key, exception: {e}"
