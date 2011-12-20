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
            (r"/", MainHandler)
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


##########   /*     */   ##########


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        c = pymongo.Connection('localhost')
        db = c.shows
        shows = list()
        # for a in db.shows.find().limit(10):
        #     shows.append( a )

        self.render( "index.html", shows=shows )


##########   /*     */   ##########


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()