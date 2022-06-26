#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import asyncio
from typing import Optional

async def stock_price(symbol: str) -> Optional[str]:
    url = f"https://finance.yahoo.com/quote/{symbol}/"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    price_els = soup.select("[data-test=\"qsp-price\"]")
    if len(price_els) < 1:
        return None

    return price_els.pop().text

async def main():
    tickers =  [('BTC-USD', 'BTC'), ('^BVSP', 'IBOV'), ('BRL=X', 'USD')]
    prices = await asyncio.gather(*list(map(lambda ticker: stock_price(ticker[0]), tickers)))
    output = []

    for i, (_, name) in enumerate(tickers):
        if prices[i] is None:
            continue

        output.append(f"{name}: {prices[i]}")

    print(" ".join(output))

if __name__ == "__main__":
    asyncio.run(main())
