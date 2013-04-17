#!/usr/local/bin/python

import sqlite3
#import scipy.stats

SATOSHIperBTC = 100000000 

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

def parse_by_addr(cursor):

	#print "Address | %s | %s | %s | %s | %s | %s" , (')

	for addr, (target, chance) in sorted(addrs.items(), key=lambda x: x[1]):
		wins = 0.0
		losses = 0.0
		refunds = 0.0
		count = 0.0
		btc_in = 0.0
		btc_out = 0.0
		for row in cursor.execute("SELECT * FROM bets WHERE satoshi_addr = ?" , [addr]):
			if row[11] == 'win':
				wins += 1
			elif row[11] == 'loss':
				losses += 1
			else:
				refunds += 1

			btc_in += row[3]
			btc_out += row[10]
			count += 1

		print "%s | %d | %f | %d | %d (%f) | %d | %d | %f | %f | %f" % (addr[:8], target, chance, count, wins, (wins/count), losses, refunds, (btc_in/SATOSHIperBTC), (btc_out/SATOSHIperBTC), ((btc_in - btc_out)/SATOSHIperBTC))

def detail(cursor, addr):
	count = 0.0
	wins = 0.0
	losses = 0.0
	btc_bet = 0.0
	btc_recieved = 0.0
	for row in cursor.execute("SELECT * FROM bets WHERE payout_addr = ? OR payout_addr = ?" , ('1AozjJpfFyQqu1eru8xvQyqw1b2Yc2hwFg', '1BrF6ogCQcUNp1KKEjtVsayHKKjkco9HUf')):
		btc_bet = row[3]
		btc_recieved = row[7]
		if row[11] == 'win':
			wins += 1
			if (row[10]/SATOSHIperBTC) > 100:
				print "%s: bet of %f won %f" % (row[0], row[3]/SATOSHIperBTC, row[10]/SATOSHIperBTC)
		elif row[11] == 'loss':
			losses += 1
		count += 1

	print count
	print wins/count
	print btc_recieved/SATOSHIperBTC - btc_bet/SATOSHIperBTC




def main():
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()
	
	parse_by_addr(c)
	#detail(c, '1dice5wwEZT2u6ESAdUGG6MHgCpbQqZiy')

	conn.commit()
	conn.close()


if __name__ == '__main__':
	main()
