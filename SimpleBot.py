import pywaves as pw
import datetime
from time import sleep
import os
import configparser


class SimpleBot:
    def __init__(self):
        self.log_file = "bot.log"
        self.node = "https://nodes.wavesnodes.com"
        self.chain = "mainnet"
        self.matcher = "https://nodes.wavesnodes.com"
        self.order_fee = int(0.003 * 10 ** 8)
        self.order_lifetime = 29 * 86400  # 29 days
        self.private_key = ""
        self.amount_asset = pw.WAVES
        self.price_asset = pw.Asset("8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS")  # BTC
        self.price_step = 0.005
        self.min_amount = 1
        self.seconds_to_sleep = 15

    def log(self, msg):
        timestamp = datetime.datetime.utcnow().strftime("%b %d %Y %H:%M:%S UTC")
        s = "[{0}]:{1}".format(timestamp, msg)
        print(s)
        try:
            f = open(self.log_file, "a")
            f.write(s + "\n")
            f.close()
        except OSError:
            pass

    def read_config(self, cfg_file):
        if not os.path.isfile(cfg_file):
            self.log("Missing config file")
            self.log("Exiting.")
            exit(1)

        try:
            self.log("Reading config file '{0}'".format(cfg_file))
            config = configparser.RawConfigParser()
            config.read(cfg_file)
            self.node = config.get('main', 'node')
            self.chain = config.get('main', 'network')
            self.matcher = config.get('main', 'matcher')
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
        except OSError:
            self.log("Error reading config file")
            self.log("Exiting.")
            exit(1)


def main():
    bot = SimpleBot()
    bot.read_config("config.cfg")
    pw.setNode(node=bot.node, chain=bot.chain)
    pw.setMatcher(node=bot.matcher)
    my_address = pw.Address(privateKey=bot.private_key)

    waves_btc = pw.AssetPair(bot.amount_asset, bot.price_asset)
    while True:
        waves_balance = my_address.balance()
        bot.log("Your balance is %18d" % waves_balance)
        btc_balance = my_address.balance('8LQW8f7P5d5PZM7GtZEBgaqRPGSzS3DfPuiXrURJ4AJS')
        bot.log("Your balance is %18d" % btc_balance)
        my_address.cancelOpenOrders(waves_btc)
        order_book = waves_btc.orderbook()
        best_bid = order_book["bids"][0]["price"]
        best_ask = order_book["asks"][0]["price"]
        spread_mean_price = (best_bid + best_ask) // 2
        bid_price = spread_mean_price * (1 - bot.price_step)
        ask_price = spread_mean_price * (1 + bot.price_step)
        bid_amount = int((btc_balance / bid_price) * 10 ** pw.WAVES.decimals) - bot.order_fee
        ask_amount = int(waves_balance) - bot.order_fee

        bot.log("Best_bid: {0}, best_ask: {1}, spread mean price: {2}".format(best_bid, best_ask, spread_mean_price))

        if bid_amount >= bot.min_amount:
            bot.log("Post buy order with price: {0}, amount:{1}".format(bid_price, bid_amount))
            my_address.buy(assetPair=waves_btc, amount=bid_amount, price=bid_price, matcherFee=bot.order_fee,
                           maxLifetime=bot.order_lifetime)
        if ask_amount >= bot.min_amount:
            bot.log("Post sell order with price: {0}, ask amount: {1}".format(ask_price, ask_amount))
            my_address.sell(assetPair=waves_btc, amount=ask_amount, price=ask_price, matcherFee=bot.order_fee,
                            maxLifetime=bot.order_lifetime)

        bot.log("Sleep {0} seconds...".format(bot.seconds_to_sleep))
        sleep(bot.seconds_to_sleep)


if __name__ == "__main__":
    main()
