# Introduction

This repo contains the code for a soulbound token on the Stellar network.  It also contains the code to create base 64 encoded metadata.  This token is *fully on chain*.

The metadata is encoded onto the Stellar network via the `append_manage_data_op` function.  Note that this only allows a data fragment of up to 64 bytes.  However, we can chain a series of these and encode the metadata in chunks.  On the receiving end, we will have to recostruct those chunks.  Once reconstructed, we have a base-64 encoded string representing the metadata of the token.

# Requirements

Code has been tested on Python 3.8.  Note that there appears to be an issue with the 'Keypair' object in `stellar_base` for Python 3.10.

Third party requirements include `stellar_base`, `stellar_sdk`, and `pbkdf2` (see next section).
# Installation

`> pip install -r requirements.txt`

# Usage

The functionality encompassed by this repository includes:

1. Creating token metadata for a fully on-chain soulbound token.
2. Creating and issuing the soulbound token.

## Creating the Metadata

Code to create metadata is in the `certificate.py` file.  The steps to create the data are:

1. Create the image, given the participant's name, course name, and title of the certificate.
2. Create the rest of the metadata associated with the token

To create the token metadata:

`> python certificate.py -S <symbol> --course <course_name> --name <name> --title <certificate_title>`

**NOTE:** Token creation code will do this automatically.  It is not necessary to run the token metadata creation code in a separate step.

## Creating the Token

The process of launching the fully on-chain soulbound Stellar token includes three steps:

1. Create the keypairs for the issuer and distributer addresses.  This step is not necessary if you have these created already, just ensure that the trustline between issuer and distributer exists.
2. Register and fund the wallets.  Again, this is not necessary if you already have accounts funded.
3. Create the token and bind the metadata to it.
4. Read metadata from the blockchain.

For examples with command line arguments, see below.

- To create the keys:

`> python stellar.py -c keys -o keys.json`

- To register the keys:

`> python stellar.py -r -k keys.json -s https://horizon-testnet.stellar.org`

- To create the token:

`> python stellar.py -c token -k keys.json -s https://horizon-testnet.stellar.org -S <symbol> --course <course_name> --name <name> --title <certificate_title>`

- To read the token metadata:

`> python stellar.py -g -u <transaction_url>`
