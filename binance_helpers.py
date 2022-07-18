import json
# from aiohttp import ClientSession
from httpx import AsyncClient
from binance_endpoints import base_url_fiat, base_url_p2p, params_fiat, params_p2p

relevant_coins = [
    "USDT",
    "BTC",
    "BUSD",
    "BNB",
    "ETH",
    "DAI"
]

async def get_p2p_offers(client: AsyncClient, coin: str, fiat: str, amount: str | None, offline_test: bool = False):
    if offline_test == False:
        resp = await client.post(base_url_p2p, json=params_p2p(coin, fiat, amount))
        assert resp.status_code == 200
        return resp.json()
    else:
        with open('p2p.txt', 'r', encoding='utf-8') as f:
            return json.load(f)[coin]


async def get_fiat_cost(client: AsyncClient, fiat: str, offline_test: bool = False):
    if offline_test == False:
        resp = await client.post(base_url_fiat, json=params_fiat(fiat))
        assert resp.status_code == 200
        resp_obj = resp.json()
        fiat_cost = {}
        for x in resp_obj["data"]:
            if x["assetCode"] in relevant_coins:
                fiat_cost[x["assetCode"]] = x
        return fiat_cost
    else:
        with open('fiat.txt', 'r', encoding='utf-8') as f:
            return json.load(f)