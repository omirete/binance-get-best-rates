base_url_fiat = 'https://www.binance.com/bapi/fiat/v2/friendly/ocbs/buy/list-crypto'


def params_fiat(fiat: str):
    params = {
        "channels": ["wallet"],
        "fiat": fiat,
        "transactionType": "buy"
    }
    return params


base_url_p2p = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'


def params_p2p(coin: str, fiat: str, amount: str | None, page: int = 1, rows: int = 10):
    params = {
        "page": page,
        "rows": rows,
        "payTypes": [
            "MercadoPago",
            "MercadoPagoNew"
        ],
        "publisherType": None,
        "asset": coin,
        "tradeType": "SELL",
        "fiat": fiat,
        "merchantCheck": False,
        "transAmount": amount
    }
    return params
