import json
from csv import reader as csvreader, writer as csvwriter
from collections import namedtuple, defaultdict

import geocoder


def read_uikparams():
    data = csvreader(open('uikparams.csv'), delimiter=',')
    next(data, None)
    
    Row = namedtuple('row', 'tik, raion, uik, voters, mn_in, mn_out, koib, addr_vote, place, doma, phone, url, uikpage, addr_komissii, phone_k')
    for row in data:
        try:
            x = Row(*row[:len(Row._fields)])
        except:
            print(row)
        yield x.uik, dict(x._asdict(), koib = 'KOIB' if x.koib != '0' else '')
    #new = lambda x: Row(*x[:len(Row._fields)])
    #return {new(x).uik: new(x)._asdict() for x in data}

uikparams = dict(read_uikparams())


if __name__ == '__main__':
    src = csvreader(open('uik_spb_gps.csv'), delimiter=',')
    header = next(src, None)
    
    dst = csvwriter(open(f'uik_spb_gps2.csv', 'w+'))
    dst.writerow(header)
    
    
    Row = namedtuple('row', 'tik, uik, coords')
    #result = defaultdict(list)
    for tik, uik, coords in src:
        if coords:
            dst.writerow([tik,uik, coords])
            try:
                xy = json.loads(coords)
            except:
                print(tik, uik, coords)
                #continue
            continue
            #if not all(xy.values()):
                #raise Exception()
                #lng, lat = round(xy["lng"], 3), round(xy["lat"], 3)
                #result[f'{lng} {lat}'].append(Row(tik, uik, xy))
        if uikparams[uik]['addr_vote']:
            print(tik, uik, uikparams[uik]['addr_vote'])
            idx, city, region, mo, street, dom, *_ = uikparams[uik]['addr_vote'].split(',')
            addr = ','.join([city, region, street, dom])
            print(addr)
            gg = geocoder.yandex(addr)
            if not gg.ok:
                print('error')
                import ipdb; ipdb.sset_trace()
                continue
            coord = f'{{"lng": {gg.json["lng"]}, "lat": {gg.json["lat"]}}}'
            print('result ', gg.current_result, coord)
            dst.writerow([tik, uik, coord])
            print()
        else:
            dst.writerow([tik, uik, coords])
            print(tik, uik)
