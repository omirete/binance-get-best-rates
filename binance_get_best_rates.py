import trio
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from httpx import AsyncClient
from binance_helpers import get_fiat_cost, get_p2p_offers, relevant_coins
from functools import partial


def plot_rates(df):
    sns.set_theme(style="darkgrid")
    g = sns.lineplot(data=df)
    # plt.ylim(0, 230)
    plt.show()


async def main(offline_test: bool = False, print_table: bool = False, show_plot: bool = False) -> str:
    async with AsyncClient() as client:
        fiat_cost = await get_fiat_cost(client, "EUR", offline_test=offline_test)

        p2p_offers = {}
        for coin in relevant_coins:
            p2p_offers[coin] = await get_p2p_offers(client, coin, 'ARS', "40000", offline_test=offline_test)

        rates = {}
        msg = ''
        for coin in relevant_coins:
            price_start_currency = fiat_cost[coin]["quotation"]
            msg_line = f"{coin}:"
            rates[coin] = []
            for i in range(10):
                price_end_currency = p2p_offers[coin]["data"][i]["adv"]["price"]
                rate = float(price_end_currency) / float(price_start_currency)
                rates[coin].append(round(rate, 2))
                msg_line += f"\t{rates[coin][i]}"
            msg += f"{msg_line}\n"

        if print_table == True:
            print(msg)

        if show_plot == True:
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

        return msg


def getRatesTable() -> str:
    func = partial(main,
                   offline_test=False,
                   print_table=False,
                   show_plot=False
                   )
    rates_table = trio.run(func)
    return rates_table


if __name__ == "__main__":
    func = partial(main,
                   offline_test=False,
                   print_table=True,
                   show_plot=True
                   )
    trio.run(func)
