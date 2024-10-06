from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Tuple, Type, Union

from langchain_core.tools import BaseTool
from langchain_core.utils import guard_import
from pydantic import model_validator

if TYPE_CHECKING:
    from dendrite_sdk import Dendrite, AsyncDendrite
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from dendrite_sdk import Dendrite, AsyncDendrite
    except ImportError:
        pass


def lazy_import_dendrite_browsers() -> Tuple[Type[Dendrite], Type[AsyncDendrite]]:
    """
    Lazy import Dendrite clients.

    Returns:
        Tuple[Type[Dendrite], Type[AsyncDendrite]]:
            Dendrite and AsyncDendrite classes.
    """
    return (
        guard_import(module_name="dendrite_sdk").Dendrite,
        guard_import(module_name="dendrite_sdk").AsyncDendrite,
    )


class BaseDendriteTool(BaseTool):
    """Base class for Dendrite tools."""

    client: Optional["Dendrite"] = None
    async_client: Optional["AsyncDendrite"] = None

    @model_validator(mode="before")
    @classmethod
    def validate_browser_provided(cls, values: dict) -> Any:
        """Check that the arguments are valid."""
        lazy_import_dendrite_browsers()
        if values.get("async_client") is None and values.get("client") is None:
            raise ValueError("Either async_client or client must be specified.")
        return values

    @classmethod
    def from_client(
        cls,
        client: Union[Dendrite, AsyncDendrite],
    ) -> BaseDendriteTool:
        """Instantiate the tool."""
        lazy_import_dendrite_browsers()
        if isinstance(client, AsyncDendrite):
            return cls(client=None, async_client=client)  # type: ignore[call-arg]
        elif isinstance(client, Dendrite):
            return cls(client=client, async_client=None)  # type: ignore[call-arg]
