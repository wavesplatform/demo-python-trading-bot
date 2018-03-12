# SimpleBot

SimpleBot is a Python bot implementing a scalping trading strategy. It can work with any assets pair on the Waves DEX.

SimpleBot exploits small changes in currency prices: it buys at the mean price minus some step and sells at the mean price plus some step, in order to gain the bid/ask difference. It normally involves establishing and liquidating a position quickly, in this case within 15 seconds.

The SimpleBot with initial parameters trade on Waves-BTC pair (Waves is an amount asset and BTC is a price_asset). The spread mean price is ```(best_bid + best_ask) / 2```. The price step is ```0.5%``` from mean price. The SimpleBot place the buy order at price ```meanprice * (1 - price_step)``` and the amount ```(BTC_balance / bid_price) - order_fee```. The sell order is placed at ```meanprice * (1 + price_step)``` and the amount equal to ```Waves_balance - order_fee```.

## Installation

SimpleBot requires Python 3.x and the following Python packages:

* [PyWaves](https://github.com/PyWaves/PyWaves)
* configparser 

You can install them with

```
pip install pywaves
pip install configparser 
```

## Getting Started

You can start SimpleBot with this command:

```
python SimpleBot.py config.cfg
```

#### Configuration

Configuration file ```config.cfg``` have next set of parameters:
```node``` is the address of the fullnode

```matcher``` is the matcher address

```chain```  mainnet or testnet

```order_fee``` is the fee to place buy and sell orders

```order_lifetime``` is the maximum life time (in seconds) for an open order

```private_key``` is the private key of the trading account

```amount_asset``` and ```price_asset``` are the IDs of the traded assets pair

```price_step``` is the step of scalping relative to the mean price (proportion)
