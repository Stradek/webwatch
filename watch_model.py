from pydantic import BaseModel
from typing_extensions import TypedDict


class ItemFilter(BaseModel):
    name: str
    css_selector: str
    attribute: str = "text"
    type: str = "string"


class WatchedItem(BaseModel):
    name: str
    url: str
    cookie: str = None
    item_filters: list[ItemFilter]
    hours_to_update: int
    sort_by: str = None
    sort_order: str = None


class Watchlist(BaseModel):
    watchlist_items: list[WatchedItem]
    cookie: str = None


class ExtractedItem:
    name: str
    url: str
    keys: list[str] = []
    values_dict: dict[str, list] = {}


class ExtractedWatchlist:
    watchlist_items: list[ExtractedItem] = []
