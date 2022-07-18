import trio
import json
import os
from datetime import datetime
from httpx import AsyncClient
import trio
import pandas as pd
from binance_helpers import get_fiat_cost, get_p2p_offers, relevant_coins
import matplotlib.pyplot as plt
import seaborn as sns


def plot_rates(df):
    sns.set_theme(style="darkgrid")
    g = sns.lineplot(data=df)
    # plt.ylim(0, 230)
    plt.show()


async def main(offline_test: bool = False):
    async with AsyncClient() as client:
        fiat_cost = await get_fiat_cost(client, "EUR", offline_test=offline_test)

        p2p_offers = {}
        for coin in relevant_coins:
            p2p_offers[coin] = await get_p2p_offers(client, coin, 'ARS', "40000", offline_test=offline_test)

        rates = {}
        for coin in relevant_coins:
            price_start_currency = fiat_cost[coin]["quotation"]
            msg_line = f"{coin}:"
            rates[coin] = []
            for i in range(10):
                price_end_currency = p2p_offers[coin]["data"][i]["adv"]["price"]
                rate = float(price_end_currency) / float(price_start_currency)
                rates[coin].append(round(rate, 2))
                msg_line += f"\t{rates[coin][i]}"
            print(msg_line)

        df = pd.DataFrame(rates)
        plot_rates(df)

        if offline_test == False:
            timestamp = datetime.now().isoformat()[:19].replace(":", "-")
            folder = os.path.join('historical_retrievals', timestamp)
            os.mkdir(folder)
            with open(os.path.join(folder, 'fiat.txt'), 'w', encoding='utf-8') as f:
                f.write(json.dumps(fiat_cost))

            with open(os.path.join(folder, 'p2p.txt'), 'w', encoding='utf-8') as f:
                f.write(json.dumps(p2p_offers))

trio.run(main, (False))
