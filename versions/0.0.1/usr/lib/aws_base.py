#!/usr/bin/env python
#
# This script must be called from env var publish hooks

import sys
import os
import base64
import requests

def env_var_add(name, value):
	print "ENV_VAR_ADD: %s=%s" % (name, value)
	#with open(os.path.join('env', name), 'w') as var:
	#	var.write(value)

def cart_name(ident_var):
	return '-'.join(os.environ[ident_var].split(':')[0:3])

def url(*trailing):
	base_url = os.environ['AWS_STORE_BASE_URL']
	if not base_url.endswith('/'):
		base_url = base_url + '/'

	if trailing:
		trailing = '/'.join(trailing) + '/'

	return base_url + trailing

def _request(verb, url, secret_token, **kva):
	# use secret_token created by bin/setup to authtenticate
	access_token = base64.encodestring('%s:%s' % (os.environ['OPENSHIFT_APP_UUID'], secret_token)).strip()

	insecure = os.environ.get('INSECURE', 'false') == 'true'
	method = getattr(requests, verb)

	if 'params' not in kva:
		kva['params'] = {}
	kva['params']['cart_name'] = cart_name('OPENSHIFT_AWS_S3_IDENT')

	res = method(url, headers={'Authorization': 'Bearer %s' % access_token}, verify=not insecure, **kva)
	if not res.ok:
		raise Exception("Invalid response from server: %i: %s" % (res.status_code, res.text))
	if res.content:
		return res.json()['data']

def post(url, secret_token, **kva):
	return _request('post', url, secret_token, **kva)

def delete(url, secret_token, **kva):
	return _request('delete', url, secret_token, **kva)
