import requests


def rate(o):
    return o["rate"]


def SellBids(o):
    s = []
    for i in o["bids"]:
        s.append((i["price"], i["quantity"]))
    return min(s)


def BuyBids(o):
    s = []
    for i in o["bids"]:
        s.append((i["price"], i["quantity"]))
    return max(s)


class Marketplace:

    def __init__(self, token: str):
        self.token = token

    def infoController(self):
        url = "https://datsorange.devteam.games/info"
        header = {"token": self.token}
        return requests.get(url=url, headers=header).json()

    # return news sorted by rating
    def news1Minute(self):
        url = "https://datsorange.devteam.games/news/LatestNews1Minute"
        header = {"token": self.token}
        news = requests.get(url=url, headers=header).json()
        s = {"positive": [], "negative": []}
        for i in news:
            if i["rate"] > 0:
                s["positive"].append(i)
            else:
                s["negative"].append(i)
        s["positive"].sort(key=rate, reverse=True)
        s["negative"].sort(key=rate)
        return s

    # return news sorted by rating
    def news5Minute(self):
        url = "https://datsorange.devteam.games/news/LatestNews5Minutes"
        header = {"token": self.token}
        news = requests.get(url=url, headers=header).json()
        s = {"positive": [], "negative": []}
        for i in news:
            if i["rate"] > 0:
                s["positive"].append(i)
            else:
                s["negative"].append(i)
        s["positive"].sort(key=rate, reverse=True)
        s["negative"].sort(key=rate)
        return s

    # return news sorted by rating
    def newsLast(self):
        url = "https://datsorange.devteam.games/news/LatestNews"
        header = {"token": self.token}
        return requests.get(url=url, headers=header).json()

    # return all assets
    def assets(self):
        url = "https://datsorange.devteam.games/getSymbols"
        header = {"token": self.token}
        return requests.get(url=url, headers=header).json()

    # return all aplication where bind noot empty, sorted by max(price)
    def buyApplication(self, s):
        url = "https://datsorange.devteam.games/buyStock"
        header = {"token": self.token}
        arr = requests.get(url=url, headers=header).json()
        listApplication = []
        for i in arr:
            if i["bids"]:
                if len(s) == 0 or i["ticker"] in s:
                    listApplication.append(i)
        listApplication.sort(key=SellBids)
        return listApplication

    def sellApplication(self, s):
        url = "https://datsorange.devteam.games/sellStock"
        header = {"token": self.token}
        arr = requests.get(url=url, headers=header).json()
        listApplication = []
        for i in arr:
            if i["bids"]:
                if len(s) == 0 or i["ticker"] in s:
                    listApplication.append(i)
        listApplication.sort(key=BuyBids)
        return listApplication

    def limitPriceSell(self, symbolId, price, quantity: int):
        url = "https://datsorange.devteam.games/LimitPriceSell"
        header = {"token": self.token}
        body = {
            "symbolId": symbolId,
            "price": price,
            "quantity": quantity,
        }
        return requests.post(url=url, headers=header, json=body).json()

    def limitPriceBuy(self, symbolId, price, quantity: int):
        url = "https://datsorange.devteam.games/LimitPriceBuy"
        header = {"token": self.token}
        body = {
            "symbolId": symbolId,
            "price": price,
            "quantity": quantity,
        }
        return requests.post(url=url, headers=header, json=body).json()

    def cancelBid(self, bidId: int) -> bool:
        url = "https://datsorange.devteam.games/RemoveBid"
        header = {"token": self.token}
        body = {
            "bidId": bidId,
        }
        return requests.post(url=url, headers=header, json=body).status_code == 200

    def fastSell(self, symbolId, quantity: int):
        url = "https://datsorange.devteam.games/BestPriceSell"
        header = {"token": self.token}
        body = {
            "symbolId": symbolId,
            "quantity": quantity,
        }
        return requests.post(url=url, headers=header, json=body).json()

    def fastBuy(self, symbolId, quantity: int):
        url = "https://datsorange.devteam.games/BestPriceBuy"
        header = {"token": self.token}
        body = {
            "symbolId": symbolId,
            "quantity": quantity,
        }
        return requests.post(url=url, headers=header, json=body).json()
