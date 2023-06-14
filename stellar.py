#!/usr/bin/python

###########################################################################
#
# name          : stellar.py
#
# purpose       : Soubound token
# 
# usage         : python stellar.py <args> 
#
# description   :
#
###########################################################################

import json
import requests
from stellar_sdk import Asset
from stellar_sdk import Keypair
from stellar_sdk import Network
from stellar_sdk import Server
from stellar_sdk import Signer
from stellar_sdk import TransactionBuilder
from stellar_token_factory import TokenFactory


DISTRIBUTOR = "distributor"
ISSUER = "issuer"
RECIPIENT = "recipient" 
SERVER = "https://horizon-testnet.stellar.org" 
KEYS = "keys.json"
META = "default metadata"


def create_keys( options ) :
    print( "Creating keys" )
    keys = {}
    for key in [ DISTRIBUTOR, ISSUER, RECIPIENT ] :
        pair = Keypair.random()

        keys[ key ] = {}
        keys[ key ][ "secret" ] = pair.secret
        keys[ key ][ "public" ] = pair.public_key

    with open( options.output, 'w' ) as f :
        json.dump( keys, f, indent=2 )


def register_keys( options ) :
    print( "Registering keys" )

    keys = None
    with open( options.keys, 'r' ) as f :
        keys = json.load( f )

    server = Server( options.server )

    for key in keys :
        public_key = keys[ key ][ "public" ] 
        response = requests.get(f"https://friendbot.stellar.org?addr={public_key}")
        if response.status_code == 200:
            print(f"SUCCESS! You have a new account :)\n{response.text}")
        else:
            print(f"ERROR! Response: \n{response.text}")

        account = server.accounts().account_id(public_key).call()
        for balance in account['balances']:
            print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")


def create_token( options ) :
    print( "Creating token" )

    keys = None
    with open( options.keys, 'r' ) as f :
        keys = json.load( f )

    # Issuer account
    issuer_secret_key = keys[ "issuer" ][ "secret" ]
    issuer_public_key = keys[ "issuer" ][ "public" ]

    # Distributor account
    distributor_secret_key = keys[ "distributor" ][ "secret" ]
    distributor_public_key = keys[ "distributor" ][ "public" ]

    # Recipient account
    recipient_secret_key = keys[ "recipient" ][ "secret" ]
    recipient_public_key = keys[ "recipient" ][ "public" ]

    tf = TokenFactory( issuer_secret_key )

    tx = tf.generate_non_fungible_token( distributor_secret_key, options.symbol, metadata=options.metadata)
    print( json.dumps( tx, indent=2 ) )


def transfer_token( options ) :
    tf = TokenFactory( issuer_secret_key )
    tx = tf.transfer( options.from_address, options.to_address, options.contract )


if __name__ == "__main__" :

    import optparse
    parser = optparse.OptionParser()
    parser.add_option( "-r", "--register", dest="register", 
            action="store_true", default=False, help="Register and fund keys", metavar="BOOL" )
    parser.add_option( "-t", "--transfer", dest="transfer", 
            action="store_true", default=False, help="transfer", metavar="BOOL" )

    parser.add_option( "-c", "--create", dest="create", 
            action="store", default="", help="Create keys or token", metavar="BOOL" )
    parser.add_option( "-F", "--from", dest="from_address", 
            action="store", default="", help="From address", metavar="STRING" )
    parser.add_option( "-T", "--to", dest="to_address", 
            action="store", default="", help="To address", metavar="STRING" )
    parser.add_option( "-k", "--keys", dest="keys", 
            action="store", default=KEYS, help="Keys file", metavar="STRING" )
    parser.add_option( "-o", "--output", dest="output", 
            action="store", default=KEYS, help="Keys output file", metavar="STRING" )
    parser.add_option( "-s", "--server", dest="server", 
            action="store", default=SERVER, help="Keys output file", metavar="STRING" )
    parser.add_option( "-S", "--symbol", dest="symbol", 
            action="store", default="SOUL", help="Token symbol", metavar="STRING" )
    parser.add_option( "-l", "--limit", dest="limit", 
            action="store", default="100", help="Token limit", metavar="STRING" )
    parser.add_option( "-m", "--metadata", dest="metadata", 
            action="store", default=META, help="Token metadata", metavar="STRING" )
    ( options, args ) = parser.parse_args()


    if options.create :
        if options.create == "keys" :
            create_keys( options )
        if options.create == "token" :
            create_token( options )

    if options.register :
        register_keys( options )

    if options.transfer :
        transfer_token( options )
