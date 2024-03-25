from sinopac_stock.utils import lookup_stock_name


def test_find_the_stock_name():
    assert lookup_stock_name("00878") == "國泰永續高股息"
    assert lookup_stock_name("00919") == "群益台灣精選高息"
    assert lookup_stock_name("00929") == "復華台灣科技優息"
