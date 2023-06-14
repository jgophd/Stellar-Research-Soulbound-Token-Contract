# Introduction

This repo contains the code for a soulbound token on the Stellar network.

# Installation

`> pip install -r requirements.txt`

# Usage

- To create the keys:

`> python stellar.py -c keys -o keys.json`

- To register the keys:

`> python stellar.py -r -k keys.json -s https://horizon-testnet.stellar.org`

- To create the token:

`> python stellar.py -c token -k keys.json -s https://horizon-testnet.stellar.org -S <symbol> -l <number of tokens> -m <metadata>`

- To transfer the token:

`> python stellar.py -t -F <from> -T <to> -C <credentials>`
