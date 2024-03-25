import json
import os
from typing import Dict

from dotenv import load_dotenv
import shioaji as sj
from sinopac_stock import APICredentials


def stock_info_cache_file():
    filename = "stock_infos.json"
    local_cache = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", filename
    )
    return local_cache


def load_cache():
    with open(stock_info_cache_file(), "r") as fh:
        return json.loads(fh.read())


cached_stock_info = load_cache()


def lookup_stock_name(stock_number: str) -> str:
    if stock_number not in cached_stock_info:
        return "????"
    data = cached_stock_info[stock_number]
    return data["name"]


def save_to_data(stock_infos: str):
    # save to local data
    with open(stock_info_cache_file(), "w") as fh:
        fh.write(stock_infos)


def download_stock_infos():
    cred = APICredentials.from_environment_variables()
    api = sj.Shioaji(simulation=False)
    try:
        api.login(cred.sniopac_api_key, cred.sniopac_api_secret_key)
        stocks_info = {}

        for kind in [
            api.Contracts.Stocks.TSE,
            api.Contracts.Stocks.OES,
            api.Contracts.Stocks.OTC,
        ]:
            for x in kind:
                stocks_info[x.code] = dict(code=x.code, name=x.name, symbol=x.symbol)

        save_to_data(json.dumps(stocks_info))

    finally:
        api.logout()


if __name__ == "__main__":
    load_dotenv()
    download_stock_infos()
