from bs4 import BeautifulSoup
import os

import requests
import json
import argparse

from watch_model import Watchlist, WatchedItem, ExtractedWatchlist, ExtractedItem
from utils import LogStream


log_stream = LogStream()


def extract_watchlist(watchlist: Watchlist) -> ExtractedWatchlist:
    extracted_watchlist = ExtractedWatchlist()
    for watchlist_item in watchlist.watched_item_list:
        assert watchlist_item.name is not None, log_stream.error("Watchlist item name cannot be empty")
        assert watchlist_item.url is not None, log_stream.error("Watchlist item URL cannot be empty")
        assert len(watchlist_item.filter_list) > 0, log_stream.error("Watchlist item filters cannot be empty")

        try:
            extracted_item = extract_watchlist_item(watchlist_item)
        except Exception as e:
            log_stream.error(f"Cannot extract watchlist item: {watchlist_item.name}")
            log_stream.error(e)
            raise e

        extracted_watchlist.watchlist_items.append(extracted_item)

    return extracted_watchlist


def extract_watchlist_item(item: WatchedItem) -> ExtractedItem:
    url = item.url
    item_filter_list = item.filter_list

    cookie = item.cookie

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ',
        'Accept-Language': 'pl,en-US;q=0.7,en;q=0.3',
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Content-Type": "text/html; charset=utf-8",
        "Cookie": f"{cookie}"
    }

    webpage = requests.get(url, headers=headers)
    if webpage.status_code != 200:
        log_stream.error(f"Cannot get webpage: {url}")
        log_stream.error(f"Status code: {webpage.status_code}")
        raise ConnectionError(f"Cannot get webpage: {url}")

    soup = BeautifulSoup(webpage.text, 'html.parser')

    keys = []
    values_dict = {}
    for item_filter in item_filter_list:
        css_selector = item_filter.css_selector
        selector_value_list = list(soup.select(css_selector))

        attribute = item_filter.attribute
        assert attribute != "", log_stream.error("Attribute cannot be empty")
        if attribute == "text":
            found_values = [value.text for value in selector_value_list]
        else:
            found_values = [value.get(attribute) for value in selector_value_list]

        item_type = item_filter.type
        assert item_type != "", log_stream.error("Type cannot be empty")
        if item_type == "number":
            converted_values = []
            for value in found_values:
                value = value.replace(",", ".")
                value = value.replace("zł", "")
                value = value.replace("PLN", "")
                value = value.replace("$", "")
                converted_values.append(float(value))
            found_values = converted_values

        keys.append(item_filter.name)

        if item.sort_by == item_filter.name:
            sorted_values = []
            if item.sort_order == "asc":
                sorted_values = sorted(found_values)
            elif item.sort_order == "desc":
                sorted_values = sorted(found_values, reverse=True)
            else:
                raise ValueError(f"Sort order was specified with {item.sort_order}. Sort order must be 'asc' or 'desc'")
            values_dict[item_filter.name] = sorted_values
        else:
            values_dict[item_filter.name] = found_values

    if not all(len(values_dict[key]) == len(values_dict[keys[0]]) for key in keys):
        log_stream.error(f"All keys must have the same count of values.")
        for key in keys:
            log_stream.error(f"Key: {key} has {len(values_dict[key])} values.")

        raise ValueError("All keys must have the same count of values.")

    if item.sort_by is not None and item.sort_by not in keys:
        log_stream.warning(f"'Sort by' item key: {item.sort_by} is not in keys list: {keys}.")

    extracted_item = ExtractedItem()
    extracted_item.name = item.name
    extracted_item.url = item.url
    extracted_item.keys = keys
    extracted_item.values_dict = values_dict

    return extracted_item


def log_extracted_watchlist(extracted_watchlist: ExtractedWatchlist):
    watched_item_list = extracted_watchlist.watchlist_items
    for watched_item in watched_item_list:
        keys = watched_item.keys
        values_dict = watched_item.values_dict

        first_key = keys[0]
        entries_count = len(values_dict[first_key])

        header = f"| Watched Item: {watched_item.name} | URL: {watched_item.url} | Entires Count: {entries_count} |"
        border = "=" * len(header)

        log_stream.log(border)
        # =========================================
        log_stream.log(header)
        # =========================================
        log_stream.log(border)

        for entry_index in range(entries_count):
            log_stream.log("-" * 30)
            for key in keys:
                log_stream.log(f"{watched_item.values_dict[key][entry_index]}")


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="webwatch",
        description="Webwatch is a tool for watching webpages and extracting data from them.",
        epilog="Have fun!"
    )
    parser.add_argument('-c', '--config',
                        action='store',
                        default="config/config.json",
                        required=False,
                        type=argparse.FileType('r'),
                        help="Run with config file")
    parser.add_argument('--cli',
                        action='store_const',
                        const=True,
                        default=False,
                        required=False,
                        help="Run in CLI mode")

    return parser


def main():
    stop_after_execution = False

    try:
        parser = get_parser()
        args = parser.parse_args()

        stop_after_execution = args.cli

        results_dir_path = os.path.relpath("results/")
        if not os.path.exists(results_dir_path):
            os.makedirs(results_dir_path)

        log_path = os.path.join(results_dir_path, "log.txt")

        with open(log_path, "w", encoding="utf-8") as logging_file:
            log_stream.set_log_file(logging_file)

            try:
                json_data = json.load(args.config)
            except FileNotFoundError as e:
                log_stream.error(e)
                log_stream.error("=" * 30)
                log_stream.error(f"Cannot find: {args.config} json config.")
                return
            except json.JSONDecodeError as e:
                log_stream.error(e)
                log_stream.error("=" * 30)
                log_stream.error(f"Cannot parse {args.config} json config.\nEnsure syntax is correct.")
                return

            watchlist = Watchlist(**json_data)
            extracted_watchlist = extract_watchlist(watchlist)

            log_extracted_watchlist(extracted_watchlist)
    except Exception as e:
        log_stream.error(e)
    finally:
        if not stop_after_execution:
            input()


if __name__ == "__main__":
    main()
