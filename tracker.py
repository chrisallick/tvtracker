#!/usr/bin/env python

from datetime import date, datetime
from tvrage import api

# today = date.today()

class TVTracker(object):

    def create( self, query, last_viewed ):
        show = api.Show(query)
        data = {}
        if show:
            data = {}
            data['title'] = show.name
            data['link'] = show.link
            data['sid'] = show.showid
            data['last_checked'] = date(2012,1,1).isoformat()
            data['new_eps'] = list()
            data['key'] = query
            data['last_viewed'] = last_viewed

            ep = show.latest_episode
            temp = {}
            temp['new_or_old'] = ""

            if ep.number < 10:
                temp['number'] = "0"+str(ep.number)
            else:
                temp['number'] = str(ep.number)

            if ep.season < 10:
                temp['season'] = "0"+str(ep.season)
            else:
                temp['season'] = str(ep.season)

            data['latest'] = "s"+temp['season']+"e"+temp['number']

            if data['latest'] == data['last_viewed']:
                temp['new_or_old'] = "old"

            if temp['number'] > data['last_viewed'][4:] and temp['season'] >= data['last_viewed'][1:3]:
                temp['new_or_old'] = "new"
            else:
                temp['new_or_old'] = "old"


            temp['link'] = "/getnzb?query=" + show.name + " s" + temp['season'] + "e" + temp['number']
            data['new_eps'].append( temp )
        return data
    
    def update( self, shows ):
        for show in shows:
            print show

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