"""Dendrite web browser toolkit."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Type, Union, cast

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict, model_validator

from langchain_community.tools.dendrite.base import (
    BaseDendriteTool,
    lazy_import_dendrite_browsers,
)
from langchain_community.tools.dendrite import (
    Goto,
    Ask,
    Extract,
    Fill,
    FillFields,
    Download,
    Upload,
    Click,
)

if TYPE_CHECKING:
    from dendrite_sdk import Dendrite, AsyncDendrite
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from dendrite_sdk import Dendrite, AsyncDendrite
    except ImportError:
        pass


class DendriteToolkit(BaseToolkit):
    """Toolkit for Dendrite tools.

    **Security Note**: This toolkit provides code to control a web-browser using Dendrite.

        Careful if exposing this toolkit to end-users. The tools in the toolkit
        are capable of navigating to arbitrary webpages, asking questions about
        the current page, and even performing downloads and uploads.

        If exposing to end-users, consider limiting network access to the
        server that hosts the agent.

        Remember to scope permissions to the minimal permissions necessary for
        the application. If the default tool selection is not appropriate for
        the application, consider creating a custom toolkit with the appropriate
        tools.

        See https://python.langchain.com/docs/security for more information.

    Parameters:
        client: Optional. The sync Dendrite client. Default is None.
        async_client: Optional. The async Dendrite client. Default is None.
    """

    client: Optional["Dendrite"] = None
    async_client: Optional["AsyncDendrite"] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="forbid",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_imports_and_client_provided(cls, values: dict) -> Any:
        """Check that the arguments are valid."""
        lazy_import_dendrite_browsers()
        if values.get("async_client") is None and values.get("client") is None:
            raise ValueError("Either async_client or client must be specified.")
        return values

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        tool_classes: List[Type[BaseDendriteTool]] = [
            Goto,
            Ask,
            Extract,
            Fill,
            FillFields,
            Download,
            Upload,
            Click,
        ]

        tools = [
            (
                tool_cls.from_client(client=self.client)
                if self.client is not None
                else (
                    tool_cls.from_client(client=self.async_client)
                    if self.async_client is not None
                    else None
                )
            )
            for tool_cls in tool_classes
            if (self.client is not None or self.async_client is not None)
        ]
        return cast(List[BaseTool], [tool for tool in tools if tool is not None])

    @classmethod
    def from_client(
        cls,
        client: Union[Dendrite, AsyncDendrite],
    ) -> DendriteToolkit:
        """Convenient method to instantiate the toolkit with a Dendrite client.

        Args:
            client: Optional. The sync or async client. Default is None.

        Returns:
            The toolkit.
        """

        # This is to raise a better error than the forward ref ones Pydantic would have
        lazy_import_dendrite_browsers()
        if isinstance(client, AsyncDendrite):
            return cls(client=None, async_client=client)
        elif isinstance(client, Dendrite):
            return cls(client=client, async_client=None)
