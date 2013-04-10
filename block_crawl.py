#!/usr/local/bin/python

import json
import requests
import pprint

SATOSHIperBTC = 100000000  # satoshi unit

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


def main():
	txs_to_st = {}
	txs_from_st = {}

	for block_num in range(230500, 230505):
		url = 'http://blockchain.info/block-height/%d?format=json' % block_num
		r = requests.get(url)
		raw_json = json.loads(r.text)
		block =  raw_json['blocks'][0]
		print 'Examining block %d' % block_num
		for tx in block['tx']:
			#pprint.pprint(tx, indent=4)
			for output in tx['out']:
				if output['type'] != 0:
					continue
				if output['addr'] not in addrs:
					continue
				if tx['tx_index'] not in txs_to_st:
					txs_to_st[tx['tx_index']] = (output['addr_tag'], output['value'])
					#print '#### %s recieved %s satoshi in TX %s' % (output['addr_tag'], output['value'], tx['tx_index'])

	for block_num in range(230500, 230510):
		url = 'http://blockchain.info/block-height/%d?format=json' % block_num
		r = requests.get(url)
		raw_json = json.loads(r.text)
		block =  raw_json['blocks'][0]
		print 'Examining block %d' % block_num
		for tx in block['tx']:
			for prev_out in tx['inputs']:
				for key, value in prev_out.items():
					if value['tx_index'] in txs_to_st and value['addr'] in addrs:
						txs_from_st[tx['tx_index']] = (value['addr_tag'], value['value'])
						#print '#### %s sent %s satoshi in TX %s to pay back TX %s' % (value['addr_tag'], value['value'], tx['tx_index'], value['tx_index'])


	print len(txs_to_st)
	print len(txs_from_st)


if __name__ == '__main__':
	main()