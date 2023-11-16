from pydantic import BaseModel
from typing_extensions import TypedDict


class WatchedItemFilter(BaseModel):
    """
    WatchedItemFilter has css selectors used to gather item from the website's html code.
    Specified in "filter_list".

    Parameters:
        **name** (str): Name of the item filter.

        **css_selector** (str): CSS selector of the item filter.

    Optional Parameters:
        **attribute** (str): Attribute of the item filter.

        Available values: "text" or "title".

        Default: "text".

        **type** (str): Type of the item filter. Depending on type, different sort mechanism will be used.

        Available values: "string" or "number".

        Default: "string".
    """

    name: str
    css_selector: str
    attribute: str = "text"
    type: str = "string"


class WatchedItem(BaseModel):
    """
    WatchedItem is a single item to watch on a given website.
    Specified in "watched_item_list".

    Parameters:
        **name** (str): Name of the item.

        **url** (str): URL of the item.

        **filter_list** (list[WatchedItemFilter]): List of item filters.

    Optional Parameters:
        **cookie** (str): Cookie to use.

        **sort_by** (str): ItemFilter name to sort by.

        **sort_order** (str): Sort order.

        Available values: "asc" or "desc".
    """

    name: str
    url: str
    filter_list: list[WatchedItemFilter]
    cookie: str = None
    sort_by: str = None
    sort_order: str = None


class Watchlist(BaseModel):
    """
    Watchlist is a root of json file.

    Parameters:
        **watched_item_list** (list[WatchedItem]): List of watched items.
    """

    watched_item_list: list[WatchedItem]


class ExtractedItem:
    name: str
    url: str
    keys: list[str] = []
    values_dict: dict[str, list] = {}


class ExtractedWatchlist:
    watchlist_items: list[ExtractedItem] = []
