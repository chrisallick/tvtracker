#!/usr/bin/env python

from datetime import date, datetime
from tvrage import quickinfo

shows = {
            'Homeland': 'homeland 2011',
            'Sons of Anarchy': 'sons of anarchy 2011',
            'Bored to Death': 'bored to death 2011',
            'Revenge': 'revenge 2011',
            'Hell on Wheels': 'hell on wheels 2011',
            'Star Wars: The Clone Wars': 'star wars the clone wars 2011',
            'The Walking Dead': 'the walking dead 2011',
            'Boardwalk Empire': 'boardwalk empire 2011',
            'South Park': 'south park 2011',
            'Parks and Recreation': 'parks and recreation 2011',
            'The Office': 'the office 2011',
            'Modern Family': 'modern family 2011',
            'Supernatural': 'supernatural 2011',
            'The Vampire Diaries': 'vampire diaries 2011'
        }

today = date.today()

for k,v in shows.iteritems():
    qi = quickinfo.fetch(v)
    print "%s:" % k
    if 'Next Episode' in qi:
        later = datetime.strptime( qi['Next Episode'][2], "%b/%d/%Y").date()
        days = (later - today).days
        print "\tNext Episode: %s days" % days
    elif 'Latest Episode' in qi:
        earlier = datetime.strptime( qi['Latest Episode'][2], "%b/%d/%Y").date()
        days = (today - earlier).days
        print "\tLast Episode: %s day(s) ago" % days
    else:
        print "\tNext Episode: None Available"