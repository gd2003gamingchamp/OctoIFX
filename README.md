# OctoIFX [0.4.0-beta2](https://github.com/gd2003gamingchamp/OctoIFX/tree/dev/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/OctoBot.svg)](https://pypi.python.org/pypi/OctoBot/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e07fb190156d4efb8e7d07aaa5eff2e1)](https://app.codacy.com/gh/gd2003gamingchamp/OctoIFX?utm_source=github.com&utm_medium=referral&utm_content=gd2003gamingchamp/OctoIFX&utm_campaign=Badge_Grade_Dashboard)[![Downloads](https://pepy.tech/badge/octobot/month)](https://pepy.tech/project/octobot)
[![Dockerhub](https://img.shields.io/docker/pulls/drakkarsoftware/octobot.svg)](https://hub.docker.com/r/drakkarsoftware/octobot)
[![Coverage Status](https://coveralls.io/repos/github/Drakkar-Software/OctoBot/badge.svg?branch=dev)](https://coveralls.io/github/gd2003gamingchamp/OctoIFX?branch=dev)
[![OctoBot-CI](https://github.com/gd2003gamingchamp/OctoIFX/workflows/OctoBot-CI/badge.svg)](https://github.com/gd2003gamingchamp/OctoIFX/actions)
[![Build Status](https://cloud.drone.io/api/badges/Drakkar-Software/OctoBot/status.svg)](https://cloud.drone.io/gd2003gamingchamp/OctoIFX)


![Web Interface](../assets/web-interface.gif)
## Description
OctoIFX is a powerful fully modular open-source cryptocurrency trading robot.

This repository contains all the features of the bot (trading tools, user interfaces, services, ...).
[OctoIFX's tentacles](https://github.com/gd2003gamingchamp/OctoIFX-tentacles) contains the bot's strategies.

To install OctoBot with its tentacles, just use the [launcher](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Installation#octobot-launcher) and your OctoIFX is ready ! 

## Your OctoIFX
<a href="https://github.com/gd2003gamingchamp/OctoIFX/blob/assets/telegram-interface.png"><img src="../assets/telegram-interface.png" height="414" alt="Telegram interface"></a>
[![Twitter Interface](../assets/twitter-interface.png)](https://twitter.com/HerklosBotCrypt)

OctoBot is highly customizable using its configuration and tentacles system. 
You can build your own bot using the infinite [configuration](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Configuration) possibilities such as 
**technical analysis**, **social media processing** or even **external statistics management** like google trends.

OctoBot is **AI ready**: Python being the main language for OctoBot, it's easy to integrate machine-learning libraries such as [Tensorflow](https://github.com/tensorflow/tensorflow) or
any other lib and take advantage of all the available data and create a very powerful trading strategy. 

Octobot's main feature is **evolution** : you can [install](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Tentacle-Manager), 
[modify](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Customize-your-OctoIFX) and even [create](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Customize-your-OctoIFX) any tentacle you want to build your ideal cryptocurrency trading robot. You can even share your OctoBot evolutions !

## Installation
OctoBot's installation is **very simple**... because **very documented** ! See the [OctoBot Wiki](https://github.com/gd2003gamingchamp/OctoIFX/wiki) for more info.

#### [With executable](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Installation)
- Open the OctoBot-Binary [release page](https://github.com/gd2003gamingchamp/OctoIFX-Binary/releases)
- Open the latest release **Assets** panel
- Download the OctoBot executable for your platform
- Start OctoBot

#### [With Docker](https://github.com/gd2003gamingchamp/OctoIFX/wiki/With-Docker)
Self hosting with docker :
```
docker run -itd --name OctoBot -p 80:5001 drakkarsoftware/octobot:0.4.0-stable
```
And then open [http://localhost](http://localhost).

#### [With python sources](https://github.com/gd2003gamingchamp/OctoIFX/wiki/With-Python-only) (unix)
- Install python3.8 (https://www.python.org/downloads/)
```
git clone git@github.com:gd2003gamingchamp/OctoIFX.git && cd OctoIFX
pip3 install -r requirements.txt
python3 start.py
```

#### One click deployment
[![Deploy to DO](https://mp-assets1.sfo2.digitaloceanspaces.com/deploy-to-do/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/gd2003gamingchamp/OctoIFX/tree/master&refcode=40c9737100b1)

Get 60-day free hosting by registering with [OctoBot referral link](https://m.do.co/c/40c9737100b1).

## Exchanges
[![Binance](../assets/binance-logo.png)](https://www.binance.com)
[![Bitmex](../assets/bitmex-logo.png)](https://bitmex.com)
[![Bitmax](../assets/bitmax-logo.png)](https://bitmax.io)
[![Coinbase](../assets/coinbasepro-logo.png)](https://pro.coinbase.com)
[![Kucoin](../assets/kucoin-logo.png)](https://www.kucoin.com)
[![Bitfinex](../assets/bitfinex-logo.png)](https://www.bitfinex.com)
[![Bittrex](../assets/bittrex-logo.png)](https://bittrex.com)

OctoIFX supports many [exchanges](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Exchanges#octobot-official-supported-exchanges) thanks to the [ccxt library](https://github.com/ccxt/ccxt). 
To activate trading on an exchange, just configure OctoBot with your api keys as described [on the wiki](https://github.com/gd2003gamingchamp/OctoIFX/wiki/Exchanges).

## Disclaimer
Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR OWN RISK. THE AUTHORS 
AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS. 

Always start by running a trading bot in simulation mode and do not engage money
before you understand how it works and what profit/loss you should
expect.

Do not hesitate to read the source code and understand the mechanism of this bot.

## Sponsors
Rob Mehism
