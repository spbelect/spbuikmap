#!/usr/bin/env python
import json
from collections import namedtuple, defaultdict
from csv import reader as csvreader

import responder

import environ

env = environ.Env()

SRC_DIR = environ.Path(__file__) - 1  # src/

env.read_env(SRC_DIR('env-local'))

DEBUG = env.bool('WEB_DEBUG', default=False)


app = responder.API(debug=True)

 #{ "type": "FeatureCollection",
    #"features": [
      #{ "type": "Feature",
        #"geometry": {"type": "Point", "coordinates": [102.0, 0.5]},
        ##"properties": {"prop0": "value0"}
        #},


def read_coords():
    csv = csvreader(open('uik_spb_gps.csv'), delimiter=',')
    next(csv, None)  # skip the headers
    
    Row = namedtuple('row', 'tik, uik, coords')
    result = defaultdict(list)
    for tik, uik, coords in csv:
        if coords:
            try:
                xy = json.loads(coords)
            except:
                print(tik, uik, coords)
                continue
            if all(xy.values()):
                lng, lat = round(xy["lng"], 4), round(xy["lat"], 4)
                #xy = {'lng': float(xy['lng']), 'lat': float(xy['lat'])}
                #result[f'{xy["lng"]} {xy["lat"]}'].append(Row(tik, uik, coords)._asdict())
                result[f'{lng} {lat}'].append(Row(tik, uik, xy))
                #yield 
    return result
    #return {Row(*x).uik: Row(*x) for x in csv}


@app.route("/uiks_geo.json")
async def uiks_geo(req, resp):
    coords = read_coords()
    #resp.media = {x.uik: x._asdict() for x in coords}
    #import ipdb; ipdb.sset_trace()
    fts = [ 
            { "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [uiks[0].coords['lng'], uiks[0].coords['lat'],]},
        #"properties": {"prop0": "value0"}
        } for uiks in coords.values()
    ]
    resp.media = { 
        "type": "FeatureCollection",
        "features": [{ 
            "type": "Feature",
            "geometry": {
                "type": "Point", 
                "coordinates": [uiks[0].coords['lng'], uiks[0].coords['lat'],]
            },
            "properties": {
                "label": ' '.join(x.uik for x in uiks),
                "uiks": [dict(uikparams.get(x.uik, {}), uik=x.uik, coords=x.coords) for x in uiks]
            }
        } for uiks in coords.values()]
    }

#@app.route("/uiks.json")
#async def uiks(req, resp):
    #coords = read_coords()
    ##resp.media = {x.uik: x._asdict() for x in coords}
    #resp.media = coords

@app.route("/")
async def home(req, resp):
    resp.content = app.template('home.html', env=env)


#http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=4784001162553
#http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=4784001269007

def read_uikparams():
    data = csvreader(open('uikparams.csv'), delimiter=',')
    next(data, None)  # skip the headers
    
    Row = namedtuple('row', 'tik, raion, uik, voters, mn_in, mn_out, koib, addr_vote, place, doma, phone, url, uikpage, addr_komissii, phone_k')
    new = lambda x: Row(*x[:len(Row._fields)])
    for row in data:
        try:
            x = Row(*row[:len(Row._fields)])
        except:
            print(row)
            #raise
        #x.
        yield x.uik, dict(x._asdict(), koib = 'KOIB' if x.koib != '0' else '')
    #return {new(x).uik: new(x)._asdict() for x in data}

uikparams = dict(read_uikparams())

if __name__ == '__main__':
    app.run(debug=DEBUG, port=env('PORT', default=8000))