# -*- coding: utf-8 -*-

import httplib2
import json
import iso8601
import datetime

class Forcast:
    def __init__(self, data):
        self.max = int(data['temperature']['max']['celsius'])
        self.maxLabel = "%d℃" %(self.max)
        self.min = None
        self.minLabel = "-"
        if data['temperature']['min'] is not None:
            self.min = int(data['temperature']['min']['celsius'])
            self.minLabel = "%d℃" %(self.min)

        dt = iso8601.parse_date(data['date'])
        self.date = datetime.date(dt.year, dt.month, dt.day)
        self.dateLabel = data['dateLabel']
        self.image = data['image']['url']
        self.telop = data['telop']


def get_forecasts(city_id='130010'):
    # 東京
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=%s' %(city_id)

    h = httplib2.Http('.cache')
    response, content = h.request(url)

    if response.status != 200:
        return []

    data  = json.loads(content.decode('utf-8'))

    forecasts = []
    for d in data['forecasts']:
        forecasts.append( Forcast(d) )

    return forecasts

if __name__ == '__main__':
    print(get_forecasts())


