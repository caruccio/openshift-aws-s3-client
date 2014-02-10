#!/usr/bin/python2.6

from pbkdf2 import PBKDF2
from hashlib import sha256 as SHA256
import base64
import string
import random

def random_string(size):
	chars = string.ascii_letters + string.digits
	return ''.join(random.choice(chars) for x in range(size))


def pbkdf2_encode(password, salt=None, iterations=10000):
	salt = salt or random_string(12)
	iterations = int(iterations)
	hash = PBKDF2(password, salt, iterations, SHA256).read(32)
	hash = base64.b64encode(hash)
	return "pbkdf2_sha256$%d$%s$%s" % (iterations, salt, hash)

if __name__ == '__main__':
	import sys
	try:
		print pbkdf2_encode(*sys.argv[1:]),
	except:
		print >>sys.stderr, "Invalid or missing parameters: password [salt, [iterations]]"
		sys.exit(1)
