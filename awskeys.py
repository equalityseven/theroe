#!/usr/bin/env python
# https://github.com/spjwebster/keychain.py.git
import keychain
import getpass
import sys
import os


def setkeys():
	password = getpass.getpass('Password:')
	
	if password != getpass.getpass('Password (again):'):
		sys.exit("Passwords did not match")

	k = keychain.Keychain()
	v,m = k.create_keychain('AWS',password)
	if not v:
		print "Please address the following error to continue."
		sys.exit('Failed: %s' % m)

	access_key = raw_input('Enter AWS access_key: ')
	secret_key = raw_input('Enter AWS secret_key: ')

	k.set_generic_password('AWS','access_key',access_key,'boto_access_key')
	k.set_generic_password('AWS','secret_key',secret_key,'boto_secret_key')
	return  k.lock_keychain('AWS')[0]


def getkeys():
	k = keychain.Keychain()

	try:
		access = k.get_generic_password('AWS','access_key', 'boto_access_key')
		secret = k.get_generic_password('AWS','secret_key', 'boto_secret_key')

		print 'AWS_ACCESS_KEY=%s' % access['password'],
		print 'AWS_SECREY_KEY=%s' % secret['password']

	except keychain.KeychainException, e:
		print "Somthing went wrong, try running this script with -h"
		sys.exit(e)


if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(
			description='Example: $ export $(./awskeys.py)')

	parser.add_argument("-k", 
			"--keyring", 
			action="store_true",
			help="Create an entry in your OSX keyring")

	parser.add_argument("-c", 
			"--clean", 
			action="store_true",
			help="Remove AWS enviroment varibles")

	args = parser.parse_args()

	if args.clean:
		print 'unset AWS_ACCESS_KEY AWS_SECREY_KEY'
		sys.exit()

	if args.keyring:
		setkeys()
	
	getkeys()

