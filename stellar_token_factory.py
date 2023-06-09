#!/usr/bin/python

###########################################################################
#
# name          : stellar_token_factory.py
#
# purpose       : token factory 
# 
# usage         : from import stellar_token_factory import TokenFactory
#
# description   :
#
###########################################################################

import io
import json
import time
from stellar_base.builder import Builder
from stellar_base.keypair import Keypair



class TokenFactory(object):

    def __init__(self, issuer_secret, network='TESTNET'):
        self.issuer_secret = issuer_secret
        self.issuer_keypair = Keypair.from_seed(issuer_secret)
        self.network = network

    def generate_non_fungible_token(self, initial_owner_secret, token_symbol, metadata=None):
        owner_keypair = Keypair.from_seed(initial_owner_secret)
        # First we generate the token trustline on the network
        self.create_trustline(initial_owner_secret, token_symbol )
        # Next we send exactly 0.0000001 to the initial owner
        return self.create_token_and_lock_account(
           token_symbol,
           owner_keypair.address().decode(),
           metadata
        )

    def create_trustline(self, secret, token_symbol ):
        builder = Builder(secret=secret, network=self.network)
        builder.append_trust_op(
            self.issuer_keypair.address().decode(),
            token_symbol,
            limit='0.0000001'
        )
        builder.sign()
        return builder.submit()

    def create_token_and_lock_account(self, token_symbol, owner_address, metadata):
        # Setup the base transaction
        builder = Builder(
            secret=self.issuer_secret,
            network=self.network
        )
        # Append relevant payment ops
        chunk_size = 64
        metadata_chunks = [ metadata[ i : i + chunk_size ] for i in range( 0, len( metadata ), chunk_size ) ]
        for i, chunk in enumerate( metadata_chunks ) :
            key = f"metadata_{i}"
            builder.append_manage_data_op( key, chunk )
            
        builder.append_payment_op(
            owner_address,
            '0.0000001',
            token_symbol,
            self.issuer_keypair.address().decode()
        )
        builder.append_set_options_op( master_weight=0 )
        builder.sign()
        return builder.submit()
