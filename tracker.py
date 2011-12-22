#!/usr/bin/env python

from datetime import date, datetime
from tvrage import api

# today = date.today()

class TVTracker(object):

    def create( self, query ):
        show = api.Show(query)
        data = {}
        if show:
            data = {}
            data['title'] = show.name
            data['link'] = show.link
            data['sid'] = show.showid
            data['last_checked'] = date(2011,12,19).isoformat()
            data['new_eps'] = list()
            data['key'] = query

            ep = show.latest_episode
            temp = {}
            #short hand?
            #when-true if boolean-value else when-false
            if ep.number < 10:
                temp['number'] = "0"+str(ep.number)
            else:
                temp['number'] = str(ep.number)
            
            if ep.season < 10:
                temp['season'] = "0"+str(ep.season)
            else:
                temp['season'] = str(ep.season)

            data['new_eps'].append( temp )
        return data

    def search( self, query ):
        data = {}
        try:
            show = api.Show( query )
            if show:
                data['title'] = show.name
                data['link'] = show.link
            return data            
        except:
            return {'error':'show not found'}