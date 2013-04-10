#!/usr/local/bin/python

import sqlite3


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
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()

	for addr, chance in addrs.items():
		print 'Getting stats for %s which has a win percentage of %f' % (addr, chance)
		wins = 0.0
		losses = 0.0
		count = 0.0
		for row in c.execute("SELECT * FROM bets WHERE satoshi_addr = ?" , [addr]):
			if row[-1] == 'win':
				wins += 1
			else:
				losses += 1
			count += 1
		print ' wins: %d' % wins
		print ' losses: %d' % losses
		win_percentage = (float(wins/count) * 100.0)
		if count:
			print ' win percentage:  %f' % win_percentage
			if win_percentage > chance:
				print 'Betters are beating satoshi by %s percentage points.\n' % (win_percentage - chance)
			elif win_percentage < chance:
				print 'Betters are losing to satoshi by %s percentage points.\n' % (chance - win_percentage)
			else:
				print 'Win percentages match published chances.\n'


if __name__ == '__main__':
	main()