"""
from flask import Blueprint, render_template
from ares.Lib import Ares

cache = Blueprint("cache", __name__, url_prefix="/cache")

@cache.route("/")
def index():
    aresObj = Ares.Report()
    aresObj.title(1, 'CACHE')
    return render_template('ares_template.html', content=aresObj.html(None))

"""

from datetime import datetime, timedelta

from click import echo


class AresCache(dict):

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, value, lifetime=3600, owner="AresCache"):
        data = {"value": value, "lifetime": lifetime, "owner": owner, "update": datetime.now(), "expiry": datetime.now() + timedelta(seconds=lifetime) if lifetime>0 else ""}
        return dict.__setitem__(self, key, data)

    def __getitem__(self, key):
        data = self[key]
        if data["expiry"] > datetime.now():
            dict.__delitem__(self, key)
            raise Exception("Key expired")
        return data

    def get(self, key):
        data = dict.get(self, key)
        if data and data["expiry"] < datetime.now():
            del self[key]
            return None
        return data

aresCache = AresCache()

def caching(f):
    def cachedFun(*args):
        ret = aresCache.get((f.__name__, args))
        if not ret:
            ret = f(*args)
            aresCache.__setitem__((f.__name__, args), ret, lifetime=10, owner=f.__module__)
            return ret
        else:
            return ret["value"]
    return cachedFun

if __name__ == '__main__':
    import time

    @caching
    def foo(a, b):
        echo("Calculate %s * %s" % (a, b))
        return a * b

    echo(aresCache)
    echo(foo(1,3))
    echo(aresCache)
    echo(foo(1,3))
    echo(aresCache)

    time.sleep(15)
    echo(foo(1,3))
    echo(aresCache)
