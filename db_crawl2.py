#!/usr/local/bin/python

import sqlite3
import numpy
import scipy.stats
import datetime
import time

SATOSHIperBTC = 100000000
MTGOX = 80.46

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

def binom_test(cursor):
	for addr, (target, chance) in sorted(addrs.items(), key=lambda x: x[1]):
		wins = 0.0
		losses = 0.0
		refunds = 0.0
		count = 0.0
		for row in cursor.execute("SELECT * FROM bets WHERE satoshi_addr = ?" , [addr]):
			if row[11] == 'win':
				wins += 1
			elif row[11] == 'loss':
				losses += 1
			else:
				refunds += 1

			count += 1

		print '-----' 
		print addr[:8]
		print scipy.stats.binom_test(wins, (count-refunds), chance)


def get_distinct_payout_addrs(cursor):
	pay_addrs = []
	for row in cursor.execute("SELECT DISTINCT payout_addr FROM bets"):
		pay_addrs.append(row[0])

	for addr in pay_addrs:
		wins = 0.0
		losses = 0.0
		refunds = 0.0
		count = 0.0
		btc_in = 0.0
		btc_out = 0.0
		for row in cursor.execute("SELECT * FROM bets WHERE payout_addr = ?", [addr]):
			if row[11] == 'win':
				wins += 1
			elif row[11] == 'loss':
				losses += 1
			else:
				refunds += 1

			btc_in += row[3]
			btc_out += row[10]
			count += 1

		valid_bets = count - refunds
		if valid_bets <= 0:
			continue
		win_pct = wins/valid_bets
		earnings = ((btc_out-btc_in)/SATOSHIperBTC) * MTGOX
		if earnings > 1000.0 and valid_bets > 50:
			print '------'
			print '%s is winning %.2f%% of the time (%d bets) - earnings: %.2f' % (addr, win_pct*100, valid_bets, earnings)


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

		p_val = scipy.stats.binom_test(wins, (count-refunds), chance)
		print "%s | %d | %f | %d | %d (%f) | %d | %d | %f | %f | %f" % (addr[:8], target, chance, count, wins, (wins/count), losses, refunds, (btc_in/SATOSHIperBTC), (btc_out/SATOSHIperBTC), ((btc_in - btc_out)/SATOSHIperBTC))
		print '\t',
		print p_val
		if (p_val < 0.01):
			print '\tREJECT NULL HYPOTHESIS'


def addr_detail(cursor, addr):
	count = 0.0
	wins = 0.0
	losses = 0.0
	refunds = 0.0
	btc_bet = 0.0
	btc_recieved = 0.0

	for row in cursor.execute("SELECT * FROM bets WHERE payout_addr = ?", [addr]):
		btc_bet += row[3]
		btc_recieved += row[10]
		if row[11] == 'win':
			wins += 1
		elif row[11] == 'loss':
			losses += 1
		else:
			refunds += 1
		count += 1

	valid_bets = count - refunds
	if valid_bets <= 0:
		return
	win_pct = wins/valid_bets
	profit = btc_in - btc_out
	roi = (profit / btc_in) * 100
	dollar_earnings = (profit / SATOSHIperBTC) * MTGOX
	print '%s made %.0f bets, won %.2f%% of the time, earned %.2f btc with a a %.2f' % (addr[:5], valid_bets, win_pct*100, dollar_earnings, roi)



def fee_analysis(cursor):
	pay_addrs = []
	for row in cursor.execute("SELECT DISTINCT payout_addr FROM bets LIMIT 1000"):
		pay_addrs.append(row[0])

	addr_fees = {}
	for addr in pay_addrs:
		print 'Getting fees for %s' % addr
		fees = []	
		for row in cursor.execute("SELECT bet_fee FROM bets WHERE payout_addr = ?", [addr]):
			fees.append(float(row[0])/SATOSHIperBTC)
		addr_fees[addr] = sum(fees)/len(fees)

	mean = numpy.mean(addr_fees.values())
	st_dev = numpy.std(addr_fees.values())
	print 'Mean of addr fee means: %.5f (std: %.8f)' % (mean, st_dev)
	high_fee_addrs = []
	for key, value in addr_fees.items():
		if (value > (mean + (st_dev * 2))):
			print 'addr: %s   fee mean: %.4f' % (key, value)
			high_fee_addrs.append(key)

	for addr in high_fee_addrs:
		addr_detail(cursor, addr)


def daterange(start_date, end_date):
	delta = end_date - start_date
	for n in range(int(delta.days)):
	#for n in range(int(delta.days * 24 + delta.seconds // 3600)):
		yield start_date + datetime.timedelta(n)
		#yield start_date + datetime.timedelta(hours=n)

def time_eval(cursor):
	start = datetime.datetime(2013, 3, 1, 0, 0, 0)
	end = datetime.datetime(2013, 3, 31, 23, 59, 59)

	for base_date in daterange(start, end):
		end_date = base_date + datetime.timedelta(1)

		start_date_int = base_date.strftime("%s")
		end_date_int = end_date.strftime("%s")

		print 'Evaulating bets between %s and %s' % (base_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S"))
		for addr, (target, chance) in sorted(addrs.items(), key=lambda x: x[1]):
			wins = 0.0
			losses = 0.0
			refunds = 0.0
			count = 0.0
			btc_in = 0.0
			btc_out = 0.0
			for row in cursor.execute('SELECT * FROM bets WHERE satoshi_addr = ? AND time >= ? AND time < ?', (addr, start_date_int, end_date_int)):
				if row[11] == 'win':
					wins += 1
				elif row[11] == 'loss':
					losses += 1
				else:
					refunds += 1

				btc_in += row[3]
				btc_out += row[10]
				count += 1

			valid_bets = count - refunds
			win_pct = 0
			if count:
				win_pct = wins/valid_bets

			profit = btc_in - btc_out
			roi = (profit / btc_in) * 100
			p_val = scipy.stats.binom_test(wins, valid_bets, chance)
			if p_val < 0.05 and win_pct > chance:
				print "%s | %d | %f | %d | %d (%f) | %d | %d | %f | %f | %f" % (addr[:8], target, chance, count, wins, win_pct, losses, refunds, (btc_out/SATOSHIperBTC), ((btc_in - btc_out)/SATOSHIperBTC))
				print '\t',
				print p_val


# def test(cursor):
# 	bets = []
# 	for row in cursor.execute('SELECT * FROM bets WHERE payout_sp_addr = ?', ['yes']):
# 		bets.append(row[0])
# 	print len(bets)

	# start = datetime.datetime(2013, 3, 1, 0, 0, 0)
	# end = datetime.datetime(2013, 3, 31, 23, 59, 59)

	# for base_date in daterange(start, end):
	# 	end_date = base_date + datetime.timedelta(1)

	# 	start_date_int = base_date.strftime("%s")
	# 	end_date_int = end_date.strftime("%s")

def test(cursor):
	bettors = []
	for row in cursor.execute('SELECT DISTINCT payout_addr FROM bets LIMIT 100'):
		bettors.append(row[0])
	print '  There were %d distinct bettors' % len(bettors)
	for bettor in bettors:
		count = 0.0
		wins = 0.0
		losses = 0.0
		refunds = 0.0
		btc_bet = 0.0
		btc_recieved = 0.0
		for row in cursor.execute("SELECT * FROM bets WHERE payout_addr = ?", [bettor]):
			btc_bet += row[3]
			btc_recieved += row[10]
			if row[11] == 'win':
				wins += 1
			elif row[11] == 'loss':
				losses += 1
			else:
				refunds += 1
			count += 1

		valid_bets = count - refunds
		if valid_bets <= 0:
			continue
		win_pct = wins/valid_bets
		profit = btc_recieved - btc_bet
		roi = (profit / btc_bet) * 100
		dollar_earnings = (profit / SATOSHIperBTC) * MTGOX
		if roi > 10:
			print '%s made %.0f bets, won %.2f%% of the time, earned $%.2f with an roi of %.2f%%' % (bettor, valid_bets, win_pct*100, dollar_earnings, roi)




def main():
	conn = sqlite3.connect('bets-223665-229007.db')
	c = conn.cursor()

	#time_eval(c)
	#fee_analysis(c)
	#get_distinct_payout_addrs(c)
	#binom_test(c)
	#parse_by_addr(c)
	#addr_detail(c)
	test(c)

	conn.commit()
	conn.close()


if __name__ == '__main__':
	main()
