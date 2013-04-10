#!/usr/local/bin/python

import sqlite3


def main():
	conn = sqlite3.connect('bets.db')
	c = conn.cursor()

	for row in c.execute("SELECT * FROM bets WHERE outcome = 'win'"):
		print row


if __name__ == '__main__':
	main()