# -*- coding: utf-8 -
#
# This file is part of restkit released under the MIT license.
# See the NOTICE for more information.


# Request Token: http://oauth-sandbox.sevengoslings.net/request_token
# Auth: http://oauth-sandbox.sevengoslings.net/authorize
# Access Token: http://oauth-sandbox.sevengoslings.net/access_token
# Two-legged: http://oauth-sandbox.sevengoslings.net/two_legged
# Three-legged: http://oauth-sandbox.sevengoslings.net/three_legged
# Key: bd37aed57e15df53
# Secret: 0e9e6413a9ef49510a4f68ed02cd

from restkit import request, OAuthFilter
from restkit.oauth2 import Consumer
from restkit.py3compat import parse_qs, parse_qsl, urlencode

from . import t


class oauth_request(object):
    oauth_uris = {
        'request_token': '/request_token',
        'authorize': '/authorize',
        'access_token': '/access_token',
        'two_legged': '/two_legged',
        'three_legged': '/three_legged'
    }

    consumer_key = 'bd37aed57e15df53'
    consumer_secret = '0e9e6413a9ef49510a4f68ed02cd'
    host = 'http://oauth-sandbox.sevengoslings.net'

    def __init__(self, utype):
        self.consumer = Consumer(key=self.consumer_key,
                            secret=self.consumer_secret)
        self.body = {
            'foo': 'bar',
            'bar': 'foo',
            'multi': ['FOO','BAR'],
            'blah': 599999
        }
        self.url = "%s%s" % (self.host, self.oauth_uris[utype])

    def __call__(self, func):
        def run():
            o = OAuthFilter('*', self.consumer)
            func(o, self.url, urlencode(self.body))
        if hasattr(run, 'func_name'):
            run.__name__ = func.__name__
        run.__name__ = func.__name__
        return run

@oauth_request('request_token')
def test_001(o, u, b):
    r = request(u, filters=[o])
    t.eq(r.status_int, 200)

@oauth_request('request_token')
def test_002(o, u, b):
    r = request(u, "POST", filters=[o])
    t.eq(r.status_int, 200)
    f = dict(parse_qsl(r.body_string()))
    t.isin('oauth_token', f)
    t.isin('oauth_token_secret', f)


@oauth_request('two_legged')
def test_003(o, u, b):
    r = request(u, "POST", body=b, filters=[o])
    t.eq(r.status_int, 200)

@oauth_request('two_legged')
def test_004(o, u, b):
    r = request(u, "GET", filters=[o])
    t.eq(r.status_int, 200)




