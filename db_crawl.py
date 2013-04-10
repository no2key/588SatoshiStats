#!/usr/local/bin/python

import sqlite3


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

	for addr, (target, chance) in addrs.items():
		print 'Getting stats for %s which has a win percentage of %f' % (addr[:9], chance)
		wins = 0.0
		losses = 0.0
		count = 0.0
		for row in cursor.execute("SELECT * FROM bets WHERE satoshi_addr = ?" , [addr]):
			if row[-1] == 'win':
				wins += 1
			else:
				losses += 1
			count += 1
		print ' wins: %d' % wins
		print ' losses: %d' % losses
		if count:
			win_percentage = float(wins/count)
			print ' win percentage:  %f' % win_percentage
			if win_percentage > chance:
				print 'Betters are beating satoshi by %s percentage points.\n' % (win_percentage - chance)
			elif win_percentage < chance:
				print 'Betters are losing to satoshi by %s percentage points.\n' % (chance - win_percentage)
			else:
				print 'Win percentages match published chances.\n'


def main():
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()
	
	parse_by_addr(c)

	conn.commit()
	conn.close()


if __name__ == '__main__':
	main()