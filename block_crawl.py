#!/usr/local/bin/python

import json
import requests
import pprint
import time
import os
import sqlite3
import datetime

SATOSHIperBTC = 100000000  # satoshi unit

# MARCH blocks
# 223665 229007

START_BLOCK = 226041
END_BLOCK = 229007

addrs = {'1dice9wVtrKZTBbAZqz1XiTmboYyvpD3t' : (64000, 0.97656),
		 '1diceDCd27Cc22HV3qPNZKwGnZ8QwhLTc' : (60000, 0.91553),
		 '1dicegEArYHgbwQZhvr5G9Ah2s7SFuW1y' : (56000, 0.85449),
 		 '1dicec9k7KpmQaA8Uc8aCCxfWnwEWzpXE' : (52000, 0.79346),
		 '1dice9wcMu5hLF4g81u8nioL5mmSHTApw' : (48000, 0.73242),
		 '1dice97ECuByXAvqXpaYzSaQuPVvrtmz6' : (32768, 0.50000),
		 '1dice8EMZmqKvrGE4Qc9bUFf9PX3xaYDp' : (32000, 0.48828),
		 '1dice7W2AicHosf5EL3GFDUVga7TgtPFn' : (24000, 0.36621),
		 '1dice7fUkz5h4z2wPc1wLMPWgB5mDwKDx' : (16000, 0.24414),
		 '1dice7EYzJag7SxkdKXLr8Jn14WUb3Cf1' : (12000, 0.18311),
		 '1dice6YgEVBf88erBFra9BHf6ZMoyvG88' : (8000, 0.12207),
		 '1dice6wBxymYi3t94heUAG6MpG5eceLG1' : (6000, 0.09155),
		 '1dice6GV5Rz2iaifPvX7RMjfhaNPC8SXH' : (4000, 0.06104),
		 '1dice6gJgPDYz8PLQyJb8cgPBnmWqCSuF' : (3000, 0.04578),
		 '1dice6DPtUMBpWgv8i4pG8HMjXv9qDJWN' : (2000, 0.03052),
		 '1dice61SNWEKWdA8LN6G44ewsiQfuCvge' : (1500, 0.02289),
		 '1dice5wwEZT2u6ESAdUGG6MHgCpbQqZiy' : (1000, 0.01526),
		 '1dice4J1mFEvVuFqD14HzdViHFGi9h4Pp' : (512, 0.00781),
		 '1dice3jkpTvevsohA4Np1yP4uKzG1SRLv' : (256, 0.00391),
		 '1dice37EemX64oHssTreXEFT3DXtZxVXK' : (128, 0.00195),
		 '1dice2zdoxQHpGRNaAWiqbK82FQhr4fb5' : (64, 0.00098),
		 '1dice2xkjAAiphomEJA5NoowpuJ18HT1s' : (32, 0.00049),
		 '1dice2WmRTLf1dEk4HH3Xs8LDuXzaHEQU' : (16, 0.00024),
		 '1dice2vQoUkQwDMbfDACM1xz6svEXdhYb' : (8, 0.00012),
		 '1dice2pxmRZrtqBVzixvWnxsMa7wN2GCK' : (4, 0.00006),
		 '1dice1Qf4Br5EYjj9rnHWqgMVYnQWehYG' : (2, 0.00003),
		 '1dice1e6pdhLzzWQq7yMidf6j8eAg7pkY' : (1, 0.00002)}

class Bet(object):
	def __init__(self):
		self.s_addr = None
		self.tx_index = None
		self.bet_tx_hash = None
		self.amt = None
		self.fee = None
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
		print 'bet_time: %d' % self.time
		print 'satoshi_addr: %s' % self.s_addr
		print 'payout_addr: %s' % self.payout_addr
		print 'bet_amt: %d' % self.amt
		print 'bet_fee: %d' % self.fee
		if self.payout:
			print 'payment: %d' % self.payout
		if self.outcome:
			print 'outcome: %s' % self.outcome

def get_fee(tx):
	btc_input = 0
	btc_output = 0
	for prev_out in tx['inputs']:
		for key, value in prev_out.items():
			btc_input += value['value']
	for output in tx['out']:
		btc_output += output['value']
	return (btc_input - btc_output)

def get_payout_addrs(tx):
	addr_list = []
	for prev_out in tx['inputs']:
		for key, value in prev_out.items():
			addr_list.append(value['addr'])
	return addr_list

def main():
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()
	try:
		c.execute('''CREATE TABLE bets (bet_tx_hash text,
									   time int,
									   satoshi_addr text,
									   bet_amount int,
									   bet_fee int,
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
			# Check if bet to satoshi dice
			for output in tx['out']:
				if output['type'] != 0:
					continue
				if output['addr'] in addrs:
					bet = Bet()
					# loop to find payout addr
					for p_output in tx['out']:
						if p_output['type'] == 0:
							if p_output['addr'] not in addrs:
								if p_output['value'] == 543210:
									bet.payout_addr = p_output['addr']

					tx_id = (tx['tx_index'], output['addr'])
					if tx_id not in bets:
						try:
							bet.s_addr = output['addr']
							bet.amt = int(output['value'])
							bet.fee = get_fee(tx)
							bet.time = int(tx['time'])
							bet.tx_index = tx['tx_index']
							bet.bet_tx_hash = tx['hash']
							bet.inputs = tx['inputs'] # save all inputs
							# need to determine payout addr
							#if tx['hash'] == '9e43048bca874635774d42fc7f7fb3046c161bd26b88c3e14c2a35c6bf32cc95':
								#print tx['inputs']

							if bet.payout_addr is None:
								bet.payout_addr = get_payout_addrs(tx)

							bets[tx_id] = bet
						except KeyError:
							print 'key error for transaction %d bet was thrown out' % tx['tx_index']


	for block_num in range(START_BLOCK, END_BLOCK+20):
		url = 'http://blockchain.info/block-height/%d?format=json' % block_num
		r = requests.get(url)
		raw_json = json.loads(r.text)
		block =  raw_json['blocks'][0]
		
		print 'Examining block %d' % block_num
		for tx in block['tx']:
			for prev_out in tx['inputs']:
				for key, value in prev_out.items():
					if value['addr'] in addrs:
						tx_id = (value['tx_index'], value['addr'])
						if tx_id in bets:
							bet = bets[tx_id]
							if bet.s_addr == value['addr']:
								bet.payout_tx_index = tx['tx_index']
								bet.payout_tx_hash = tx['hash']
								for output in tx['out']:
									#print "comparing %s and %s" % (output['addr'], bet.payout_addr)
									if output['addr'] in bet.payout_addr:
										bet.payout_addr = output['addr']
										bet.payout = int(output['value'])
										#if bet.bet_tx_hash == 'd5cc93054e1c8ea9608cea821130186d3454a4046c1618c27090bbf70b4585af':
											#bet.print_bet()
										if bet.payout == bet.amt:
											bet.outcome = 'refund'
										elif bet.payout < bet.amt:
											bet.outcome = 'loss'
										else:
											bet.outcome = 'win'

	unmatched_bets = 0
	for tx_index, bet in bets.items():

		if bet.outcome is not None:
			#bet.print_bet()
			#time.sleep(1)
			c.execute("INSERT INTO bets VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)" , (bet.bet_tx_hash, bet.time, bet.s_addr, bet.amt, bet.fee, bet.payout_addr, bet.payout_tx_hash, bet.payout, bet.outcome))
		else:
			#print bet.print_bet()
			unmatched_bets += 1
			#print 'bet %s could not be matched!' % bet.bet_tx_hash

	print len(bets)
	print unmatched_bets

	conn.commit()
	conn.close()


if __name__ == '__main__':
	main()
