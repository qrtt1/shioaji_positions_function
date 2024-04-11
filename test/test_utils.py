import inspect
import os

from pysolace import SolClient, __version__

from sinopac_stock.utils import (
    download_stock_infos,
    lookup_stock_name,
    stock_info_cache_file,
)


def test_update_cache():
    download_stock_infos()
    path = stock_info_cache_file()
    assert os.stat(path).st_size != 0


def test_find_the_stock_name():
    assert lookup_stock_name("00878") == "國泰永續高股息"
    assert lookup_stock_name("00919") == "群益台灣精選高息"
    assert lookup_stock_name("00929") == "復華台灣科技優息"


def test_signature_for_set_msg_callback():
    # pytest -k test_signature_for_set_msg_callback
    sig = inspect.signature(SolClient.set_msg_callback)
    print(__version__, sig)
    assert 2 == len(sig.parameters)
