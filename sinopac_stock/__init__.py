import threading
from typing import Dict, List

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
        api_key = os.getenv("SNIOPAC_API_KEY")
        api_secret_key = os.getenv("SNIOPAC_API_SECRET_KEY")
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

    def to_legacy_dict(self):
        from sinopac_stock.utils import lookup_stock_name

        def convert(p: PositionData):
            real_namt = int(p.quantity * p.last_price + 0.5)
            origin_namt = int(p.quantity * p.price + 0.5)
            namt = int(origin_namt + p.pnl)

            ur_ratio = ((namt / origin_namt) - 1) * 100

            return dict(
                stock=p.code,
                stocknm=lookup_stock_name(p.code),
                qty=p.quantity,
                mprice=p.last_price,
                real_namt=real_namt,
                namt=namt,
                ur_ratio=ur_ratio,
                unreal=int(p.pnl),
            )

        return convert(self)


def fetch_positions(cred: APICredentials) -> List[PositionData]:
    api = sj.Shioaji(simulation=False)
    try:
        result = api.login(cred.sniopac_api_key, cred.sniopac_api_secret_key)
        print("login status", result)
        positions: List[StockPosition] = api.list_positions(None, Unit.Share)
        return [PositionData.from_stock_position(x) for x in positions]
    except Exception as e:
        print(e)
    finally:
        api.logout()


lock = threading.Lock()


def callback(event, context):
    cfg: Dict = event
    with lock:
        positions = fetch_positions(
            APICredentials(
                sniopac_api_key=cfg.get("sniopac_api_key"),
                sniopac_api_secret_key=cfg.get("sniopac_api_secret_key"),
            )
        )
        if cfg.get("legacy", False):
            return dict(data=[x.to_legacy_dict() for x in positions])
        return [x.to_dict() for x in positions]


if __name__ == "__main__":
    load_dotenv()
    cred = APICredentials.from_environment_variables()
    print(fetch_positions(cred))
