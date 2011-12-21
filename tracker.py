#!/usr/bin/env python

from datetime import date, datetime
#from tvrage import quickinfo
from tvrage import api

# shows = {
#             'Homeland': {
#                 'show': 'homeland 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Sons of Anarchy': {
#                 'show': 'sons of anarchy 2011',
#                 'last_checked': date(2011, 12, 19)  
#             },
#             'Bored to Death': {
#                 'show': 'bored to death 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Revenge': {
#                 'show': 'revenge 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Hell on Wheels': {
#                 'show': 'hell on wheels 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Star Wars: The Clone Wars': {
#                 'show': 'star wars the clone wars 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'The Walking Dead': {
#                 'show': 'the walking dead 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Boardwalk Empire': {
#                 'show': 'boardwalk empire 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'South Park': {
#                 'show': 'south park 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Parks and Recreation': {
#                 'show': 'parks and recreation 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'The Office': {
#                 'show': 'the office 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Modern Family': {
#                 'show': 'modern family 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'Supernatural': {
#                 'show': 'supernatural 2011',
#                 'last_checked': date(2011, 12, 19)
#             },
#             'The Vampire Diaries': {
#                 'show': 'vampire diaries 2011',
#                 'last_checked': date(2011, 12, 19)
#             }
#         }

# today = date.today()

# for k,v in shows.iteritems():
#     qi = quickinfo.fetch(v)
#     print "%s:" % k
#     if 'Next Episode' in qi:
#         later = datetime.strptime( qi['Next Episode'][2], "%b/%d/%Y").date()
#         days = (later - today).days
#         print "\tNext Episode: %s days" % days
#     elif 'Latest Episode' in qi:
#         earlier = datetime.strptime( qi['Latest Episode'][2], "%b/%d/%Y").date()
#         days = (today - earlier).days
#         print "\tLast Episode: %s day(s) ago" % days
#     else:
#         print "\tNext Episode: None Available"

class TVTracker(object):

    def create( self, show ):
        show = api.Show(show)
        data = {}
        if show:
            data = {}
            data['title'] = show.name
            data['link'] = show.link
            data['last_checked'] = date(2011,12,19).isoformat()
        return data

    def search( self, show ):
        data = {}
        show = api.Show( show )
        if show:
            data['title'] = show.name
            data['link'] = show.link
        return data