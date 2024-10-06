"""Utilities for the Dendrite browser tools."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union


if TYPE_CHECKING:
    from dendrite_sdk import Dendrite, AsyncDendrite


def create_async_dendrite_client(
    auth: Optional[Union[str, List[str]]] = None,
    headless: bool = False,
    args: Optional[Dict[str, Any]] = None,
) -> AsyncDendrite:
    """
    Create an async dendrite client.

    Args:
        headless: Whether to run the browser in headless mode. Defaults to True.
        args: arguments to pass to browser.chromium.launch

    Returns:
        AsyncDendrite: The dendrite client.
    """
    from dendrite_sdk import AsyncDendrite

    client = AsyncDendrite(
        auth=auth,
        playwright_options=(
            {"headless": headless, **args} if args else {"headless": headless}
        ),
    )
    return client


def create_sync_dendrite_client(
    auth: Optional[Union[str, List[str]]] = None,
    headless: bool = False,
    args: Optional[Dict[str, Any]] = None,
) -> Dendrite:
    """
    Create a sync dendrite client.

    Args:
        headless: Whether to run the browser in headless mode. Defaults to True.
        args: arguments to pass to browser.chromium.launch

    Returns:
        SyncBrowser: The dendrite client.
    """
    from dendrite_sdk import Dendrite

    client = Dendrite(
        auth=auth,
        playwright_options=(
            {"headless": headless, **args} if args else {"headless": headless}
        ),
    )
    return client
