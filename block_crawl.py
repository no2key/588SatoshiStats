#!/usr/local/bin/python

import json
import requests
import pprint
import time
import os
import sqlite3
import datetime

SATOSHIperBTC = 100000000  # satoshi unit

START_BLOCK = 230000
END_BLOCK = 230505

addrs = {'1dice9wVtrKZTBbAZqz1XiTmboYyvpD3t' : 97.7,
		 '1diceDCd27Cc22HV3qPNZKwGnZ8QwhLTc' : 91.6,
		 '1dicegEArYHgbwQZhvr5G9Ah2s7SFuW1y' : 85.4,
 		 '1dicec9k7KpmQaA8Uc8aCCxfWnwEWzpXE' : 79.3,
		 '1dice9wcMu5hLF4g81u8nioL5mmSHTApw' : 73.2,
		 '1dice97ECuByXAvqXpaYzSaQuPVvrtmz6' : 50.0,
		 '1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp' : 48.8,
		 '1dice7W2AicHosf5EL3GFDUVga7TgtPFn' : 36.6,
		 '1dice7fUkz5h4z2wPc1wLMPWgB5mDwKDx' : 24.4,
		 '1dice7EYzJag7SxkdKXLr8Jn14WUb3Cf1' : 18.3,
		 '1dice6YgEVBf88erBFra9BHf6ZMoyvG88' : 12.2,
		 '1dice6wBxymYi3t94heUAG6MpG5eceLG1' : 9.1,
		 '1dice6GV5Rz2iaifPvX7RMjfhaNPC8SXH' : 6.1,
		 '1dice6gJgPDYz8PLQyJb8cgPBnmWqCSuF' : 4.6,
		 '1dice6DPtUMBpWgv8i4pG8HMjXv9qDJWN' : 3.1,
		 '1dice61SNWEKWdA8LN6G44ewsiQfuCvge' : 2.3,
		 '1dice5wwEZT2u6ESAdUGG6MHgCpbQqZiy' : 1.5,
		 '1dice4J1mFEvVuFqD14HzdViHFGi9h4Pp' : 0.8,
		 '1dice3jkpTvevsohA4Np1yP4uKzG1SRLv' : 0.4,
		 '1dice37EemX64oHssTreXEFT3DXtZxVXK' : 0.2,
		 '1dice2zdoxQHpGRNaAWiqbK82FQhr4fb5' : 0.1,
		 '1dice2xkjAAiphomEJA5NoowpuJ18HT1s' : 0.05,
		 '1dice2WmRTLf1dEk4HH3Xs8LDuXzaHEQU' : 0.02,
		 '1dice2vQoUkQwDMbfDACM1xz6svEXdhYb' : 0.01,
		 '1dice2pxmRZrtqBVzixvWnxsMa7wN2GCK' : 0.006,
		 '1dice1Qf4Br5EYjj9rnHWqgMVYnQWehYG' : 0.003,
		 '1dice1e6pdhLzzWQq7yMidf6j8eAg7pkY' : 0.002}

class Bet(object):
	def __init__(self):
		self.s_addr = None
		self.tx_index = None
		self.bet_tx_hash = None
		self.amt = None
		self.time = None
		self.payout = None
		self.outcome = None
		self.inputs = None
		self.payout_addr = None
		self.payout_tx_index = None
		self.payout_tx_hash = None

	def print_bet(self):
		print '-----BET----'
		print 'bet_tx_hash: %s' % self.bet_tx_hash
		print 'bet_time: %s' % datetime.datetime.fromtimestamp(self.time).strftime('%Y-%m-%d %H-%M-%S')
		print 'bet_seconds: %d' % self.time
		print 's_addr: %s' % self.s_addr
		print 'addr: %s' % self.payout_addr
		print 'bet_amt: %d' % self.amt
		print 'payment: %d' % self.payout
		print 'outcome: %s' % self.outcome

def main():
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE bets (bet_tx_hash text,
									   time int,
									   satoshi_addr text,
									   bet_amount int,
									   payout_addr text,
									   payout_tx_hash text,
									   payout_amount int,
									   outcome text)''')
	except:
		pass

	bets = {}

	for block_num in range(START_BLOCK, END_BLOCK+1):
		url = 'http://blockchain.info/block-height/%d?format=json' % block_num
		r = requests.get(url)
		raw_json = json.loads(r.text)
		block =  raw_json['blocks'][0]
		print 'Examining block %d' % block_num
		for tx in block['tx']:
			bet = Bet()
			for output in tx['out']:
				if output['type'] != 0:
					continue
				if output['addr'] not in addrs:
					if output['value'] == '54321':
						bet.payout_addr = output['addr']
						continue
					else:
						continue
				if tx['tx_index'] not in bets:
					bet.s_addr = output['addr']
					bet.amt = int(output['value'])
					bet.time = int(tx['time'])
					bet.tx_index = tx['tx_index']
					bet.bet_tx_hash = tx['hash']
					bet.inputs = tx['inputs'] # save all inputs
					# need to determine payout addr
					if bet.payout_addr is None:
						bet.payout_addr = tx['inputs'][0]['prev_out']['addr']
					bets[tx['tx_index']] = bet

	for block_num in range(START_BLOCK, END_BLOCK+1):
		url = 'http://blockchain.info/block-height/%d?format=json' % block_num
		r = requests.get(url)
		raw_json = json.loads(r.text)
		block =  raw_json['blocks'][0]
		print 'Examining block %d' % block_num
		for tx in block['tx']:
			for prev_out in tx['inputs']:
				for key, value in prev_out.items():
					if value['tx_index'] not in bets:
						continue
					bet = bets[value['tx_index']]
					if bet.s_addr == value['addr']:
						bet.payout_tx_index = tx['tx_index']
						bet.payout_tx_hash = tx['hash']
						for output in tx['out']:
							if output['addr'] == bet.payout_addr:
								bet.payout = int(output['value'])
								if bet.payout == bet.amt * .005:
									bet.outcome = 'loss'
								else:
									bet.outcome = 'win'

	for tx_index, bet in bets.items():
		if bet.outcome is not None:
			bet.print_bet()
			c.execute("INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?, ?, ?)" , (bet.bet_tx_hash, bet.time, bet.s_addr, bet.amt, bet.payout_addr, bet.payout_tx_hash, bet.payout, bet.outcome))
		else:
			print 'bet %s could not be matched!' % bet.bet_tx_hash

	conn.commit()
	conn.close()


if __name__ == '__main__':
	main()