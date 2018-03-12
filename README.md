# SimpleBot

SimpleBot is a Python bot implementing a scalping trading strategy. It can work with any assets pair on the Waves DEX.

SimpleBot exploits small changes in currency prices: it buys at the mean price minus some step and sells at the mean price plus some step, in order to gain the bid/ask difference. It normally involves establishing and liquidating a position quickly, in this case within 15 seconds.

For example, you have BTC balance ```0,00292601``` and nothing on Waves balance, we trade on Waves as an amount asset and BTC as price_asset. Best bid is ```0.00057896```, best ask is ```0.00058248``` and price step is ```0.5%``` from meanprice. The meanprice for this orderbook is ```0.00058072```. The SimpleBot place the buy order at price ```meanprice * (1 - bot.price_step)``` i.e. ```0.0005778164``` and we place the amount, equals to ```(BTC_balance / bid_price) - order_fee``` i.e. ```506090957```. And the sell order at ```meanprice * (1 + bot.price_step)``` i.e. ```58362.35999999999```, but we have no Waves, and can place only ```amount = 0```, but if we had Waves on our account too then we would set an amount equal to ```Waves_balance - order_fee```.

## Getting Started

SimpleBot requires Python 3.x and the following Python packages:

* PyWaves
* configparser 

You can install them with

```
pip install pywaves
pip install configparser 
```

You can start SimpleBot with this command:

```
python SimpleBot.py 
```

#### Designations
```node``` is the address of the fullnode

```matcher``` is the matcher address

```chain```  mainnet or testnet

```order_fee``` is the fee to place buy and sell orders

```order_lifetime``` is the maximum life time (in seconds) for an open order

```private_key``` is the private key of the trading account

```amount_asset``` and ```price_asset``` are the IDs of the traded assets pair

```log_file``` is the file where the log will be written

```price_step``` is the step of scalping relative to the mean price (proportion)
