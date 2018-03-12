import pywaves as pw
import datetime
from time import sleep
import math
import os
import configparser


class SimpleBot:
    def __init__(self):
        self.log_file = "log"
        self.node = "https://nodes.wavesnodes.com"
        self.chain = "mainnet"
        self.mather = "https://nodes.wavesnodes.com"
        self.order_fee = int(0.003 * 10 ** 8)
        self.order_lifetime = 29 * 86400 #29 days
        self.private_key = "Fc3Nn5aSjCjFLZgvqMbRv1Sznx2dhKn8JRScN5SdTwne"
        self.amount_asset = pw.WAVES
        self.price_asset = pw.Asset("8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS") #BTC
        self.price_step = 0.005

    def log(self, msg):
        timestamp = datetime.datetime.utcnow().strftime("%b %d %Y %H:%M:%S UTC")
        s = "[%s]:%s" % (timestamp, msg)
        print(s)
        try:
            f = open(self.log_file, "a")
            f.write(s + "\n")
            f.close()
        except:
            pass

    def read_config(self, cfg_file):
        if not os.path.isfile(cfg_file):
            self.log("Missing config file")
            self.log("Exiting.")
            exit(1)

        # parse config file
        try:
            self.log("%sReading config file '%s'" % cfg_file)
            config = configparser.RawConfigParser()
            config.read(cfg_file)
            self.node = config.get('main', 'node')
            self.chain = config.get('main', 'network')
            self.mather = config.get('main', 'matcher')
            self.order_fee = config.getint('main', 'order_fee')
            self.order_lifetime = config.getint('main', 'order_lifetime')

            self.private_key = config.get('account', 'private_key')
            amount_asset_id = config.get('market', 'amount_asset')
            if amount_asset_id == "WAVES":
                amount_asset_id = pw.WAVES
            self.amount_asset = amount_asset_id
            price_asset_id = config.get('market', 'price_asset')
            if price_asset_id == "WAVES":
                price_asset_id = pw.Asset(pw.WAVES)
            self.price_asset = pw.Asset(price_asset_id)

            self.log("-" * 80)
            self.log("Amount Asset ID : %s" % amount_asset_id)
            self.log("Price Asset ID : %s" % price_asset_id)
            self.log("-" * 80)
            self.log("")
        except:
            self.log("Error reading config file")
            self.log("Exiting.")
            exit(1)


def main():
    bot = SimpleBot()
    # bot.read_config("config.cfg")
    # set Matcher node to use
    pw.setNode(node=bot.node, chain=bot.chain)
    pw.setMatcher(node=bot.mather)
    my_address = pw.Address(privateKey=bot.private_key)

    waves_btc = pw.AssetPair(bot.amount_asset, bot.price_asset)
    while True:
        # get Waves balance
        bot.log("Your balance is %18d" % my_address.balance())
        # get BTC balance
        bot.log("Your balance is %18d" % my_address.balance('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS'))
        bot.log("-" * 80)
        my_address.cancelOpenOrders(waves_btc)
        order_book = waves_btc.orderbook()
        mean_spread_price = math.ceil((order_book["bids"][0]["price"] + order_book["asks"][0]["price"])/2)
        bid_price = mean_spread_price * (1 - bot.price_step)
        ask_price = mean_spread_price * (1 + bot.price_step)
        positive_or_zero = (lambda x: x if x>0 else 0)
        bid_amount = positive_or_zero(int((my_address.balance(waves_btc.a2) / bid_price) * 10 ** pw.WAVES.decimals) - bot.order_fee)
        ask_amount = positive_or_zero(int((my_address.balance() - bot.order_fee)))

        bot.log("best_bid: {0}, best_ask: {1}".format(order_book["bids"][0]["price"], order_book["asks"][0]["price"]))
        bot.log("-" * 80)

        bot.log("post buy order with price: {0}, amount:{1}".format(bid_price, bid_amount))
        my_address.buy(assetPair=waves_btc, amount=bid_amount, price=bid_price, matcherFee=bot.order_fee,
                       maxLifetime=bot.order_lifetime)
        bot.log("-" * 80)

        bot.log("post sell order with price: {0}, ask amount: {1}".format(ask_price, ask_amount))
        my_address.sell(assetPair=waves_btc, amount=ask_amount, price=ask_price, matcherFee=bot.order_fee,
                        maxLifetime=bot.order_lifetime)
        bot.log("-" * 80)

        bot.log("sleep 15 sec")
        sleep(15)  # time in seconds

if __name__ == "__main__":
    main()
