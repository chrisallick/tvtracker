#!/usr/bin/env python

import json
import os
import logging

import pymongo

from tracker import TVTracker

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)


##########   /*     */   ##########


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/search", SearchHandler),
            (r"/add", AddHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


##########   /*     */   ##########


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render( "index.html" )

class AddHandler(tornado.web.RequestHandler):
    def post(self):
        show = self.get_argument( "show", None )
        if show:
            c = pymongo.Connection('localhost')
            db = c.shows
            shows = db.shows

            tvt = TVTracker()
            data = tvt.create(show)

            old = shows.find_one({'title':data['title']})
            if not old:
                shows.insert( data )
                self.write(json.dumps({'msg':'success'}))
            else:
                self.write(json.dumps({'msg':'error'}))

class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument( "query", None )

        if query:
            tvt = TVTracker()
            self.write( json.dumps(tvt.search(query)) )
        else:
            self.render( "search.html" )


##########   /*     */   ##########


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()