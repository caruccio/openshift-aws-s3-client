#!/usr/bin/env python
#
# This script must be called from env var publish hooks

import sys
import os
import base64
import requests

def set_env_var(name, value):
	with open(os.path.join('env', name), 'w') as var:
		var.write(value)

def cart_name(ident_var):
	return '-'.join(os.environ[ident_var].split(':')[0:3])

def url(*trailing):
	base_url = os.environ['AWS_STORE_BASE_URL']
	if not base_url.endswith('/'):
		base_url = base_url + '/'

	if trailing:
		trailing = '/'.join(trailing) + '/'

	return base_url + trailing

def _request(verb, url, auth_token, **kva):
	access_token = base64.encodestring('%s:%s' % (os.environ['OPENSHIFT_APP_UUID'], auth_token)).strip()
	# ask for new credentials
	insecure = os.environ.get('INSECURE', 'false') == 'true'
	method = getattr(requests, verb)
	assert verb

	auth_cart = '-'.join(os.environ['OPENSHIFT_AWS_BASE_IDENT'].split(':')[0:3])
	if 'params' not in kva:
		kva['params'] = {}
	kva['params']['auth_cart'] = auth_cart

	res = method(url, headers={'Authorization': 'Bearer %s' % access_token}, verify=not insecure, **kva)
	if not res.ok:
		raise Exception("Invalid response from server: %i: %s" % (res.status_code, res.text))
	if res.content:
		return res.json()['data']

def post(url, auth_token, **kva):
	return _request('post', url, auth_token, **kva)

def delete(url, auth_token, **kva):
	return _request('delete', url, auth_token, **kva)
