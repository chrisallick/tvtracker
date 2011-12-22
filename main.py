#!/usr/bin/env python

import json
import os
import logging
import urllib2
from datetime import datetime, date

import pymongo

from tracker import TVTracker

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

shows = {
            'test show 2011': {
                'title': 'Test Show',
                'last_checked': date(2011, 12, 19).isoformat(),
                'link': '',
                'sid': '',
                'key': '',
                'new_eps': list()
            }
        }
account = {}

#search: query, category, maxresults, username, apikey
#http://api.nzbmatrix.com/v1.1/search.php?search=revenge+s01e10+720p+hdtv&catid=41&num=1&username={{name}}&apikey={{apikey}}
base_url = "http://api.nzbmatrix.com/v1.1/search.php?catid=41&num=1&search="
#download link: nzbid, username, apikey
base_download_url = "http://api.nzbmatrix.com/v1.1/download.php?id="

def loadShows():
    global shows
    c = pymongo.Connection('localhost')
    db = c.shows
    for show in db.shows.find():
        shows[show['key']] = show

def loadAccount():
    global account
    f = open( "info.json" )
    account = json.loads(f.read())
    f.close()
    print account['username']
    print account['apikey']


##########   /*     */   ##########


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", SearchHandler),
            (r"/add", AddHandler),
            (r"/getnzb", GetNZBHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


##########   /*     */   ##########


class GetNZBHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument( "query", None )
        if query:
            url = base_url + "+".join(query.split(" ")) + "&username=" + account['username'] + "&apikey=" + account['apikey']
            print url
            response = urllib2.urlopen(url).read()
            lines = response.split("\n")
            for line in lines:
                info = line.strip(";").split(":")
                if "NZBID" in info:
                    nzbid = info[1]
                    url = base_download_url + nzbid + "&username=" + account['username'] + "&apikey=" + account['apikey']
                    f = open( "blah.nzb", 'w').write(urllib2.urlopen( url ).read() )
                    break

##########   /*     */   ##########


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render( "index.html", shows=shows )

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        show = self.get_argument( "show", None )
        if show:
            global shows
            if show not in shows:
                c = pymongo.Connection('localhost')
                db = c.shows

                tvt = TVTracker()
                data = tvt.create(show)
                shows[show] = data
                
                db.shows.insert( data, manipulate=False )
                self.write(json.dumps(data))
            else:
                self.write(json.dumps({'error':'show exists'}))
        else:
            self.write(json.dumps({'error':'no show'}))

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument( "query", None )

        if query:
            global shows
            if query in shows:
                tvshow = shows[query]
                result = { 'title': tvshow['title'], 'link': tvshow['link'] }
            else:
                tvt = TVTracker()
                result = tvt.search(query)
            self.write( json.dumps(result) )
        else:
            self.render( "search.html" )


##########   /*     */   ##########


def main():
    loadShows()
    loadAccount()

    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()