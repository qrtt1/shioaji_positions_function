from typing import List

import shioaji as sj
from dotenv import load_dotenv
from shioaji.constant import Unit
from shioaji.position import Position, StockPosition

import os
from dataclasses import asdict, dataclass, fields


@dataclass
class APICredentials:
    sniopac_api_key: str
    sniopac_api_secret_key: str

    @staticmethod
    def from_environment_variables():
        api_key = os.getenv('SNIOPAC_API_KEY')
        api_secret_key = os.getenv('SNIOPAC_API_SECRET_KEY')
        return APICredentials(api_key, api_secret_key)


@dataclass
class PositionData:
    id: int
    code: str
    quantity: int
    price: float
    last_price: float
    pnl: float
    yd_quantity: int
    margin_purchase_amount: float
    collateral: float
    short_sale_margin: float
    interest: float

    @staticmethod
    def from_stock_position(p: StockPosition):
        field_names = {f.name for f in fields(PositionData)}
        valid_fields = {k: v for k, v in p.__dict__.items() if k in field_names}
        return PositionData(**valid_fields)

    def to_dict(self):
        return asdict(self)


def fetch_positions():
    cred = APICredentials.from_environment_variables()
    api = sj.Shioaji(simulation=False)
    result = api.login(cred.sniopac_api_key, cred.sniopac_api_secret_key)
    positions: List[StockPosition] = api.list_positions(None, Unit.Share)
    print(result)

    for p in positions:
        print(p)
        print(PositionData.from_stock_position(p))


if __name__ == '__main__':
    load_dotenv()
    fetch_positions()
