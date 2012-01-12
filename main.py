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

"""
    tvtracker:
        display shows:
            show:
                name
                link to tvrage
                episodes:
                    number
                    link to download nzb
        search for show:
            : name + season + show num
            -> enter show name
            <- show search results
        add show:
            -> select last seen episode
            add show to database and mem
        delete show:
            <- click delete
            remove from database and mem
        update show:
            look for new eps
            update show in mem and database
"""

# shows = {
#             'test show 2011': {
#                 'title': 'Test Show',
#                 'last_checked': date(2012, 1, 1).isoformat(),
#                 'link': '',
#                 'sid': '',
#                 'key': '',
#                 'last_viewed': '',
#                 'new_eps': list()
#             }
#         }
shows = {}
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
            (r"/getnzb", GetNZBHandler),
            (r"/update", UpdateHandler)
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
                    print url
                    f = open( "blah.nzb", 'w').write(urllib2.urlopen( url ).read() )
                    break
            self.write(json.dumps({'success':'show updated'}))
        else:
            self.write(json.dumps({'error':'error updating show'}))

##########   /*     */   ##########


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        global shows
        c = pymongo.Connection('localhost')
        db = c.shows
        tvt = TVTracker()
        for k,v in shows.iteritems():
            show = db.shows.find_one({'title':v['title']})
            data = tvt.create(v['title'], v['last_viewed'] )
            shows[k] = data
            show.update(data)
            db.shows.save(show)
        self.render( "index.html", shows=shows )

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        show = self.get_argument( "show", None )
        last_viewed = self.get_argument( "last-viewed", "" )
        if show:
            global shows
            if show not in shows:
                c = pymongo.Connection('localhost')
                db = c.shows

                tvt = TVTracker()
                data = tvt.create(show, last_viewed)
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

class UpdateHandler(tornado.web.RequestHandler):
    def post(self):
        query = self.get_argument( "query", None )

        if query:
            global shows
            show[query]["last_viewed"] = ""
            #update database
            self.write(json.dumps({'success':'show updated'}))
        else:
            self.write(json.dumps({'error':'error updating show'}))

# class DeleteHandler(tornado.web.RequestHandler):
#     def get(self):


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