import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,City,Activity

log = logging.getLogger(__name__)
from greencouriers.controllers.signup import search_city

class ParseTownsController(BaseController):
    def __before__(self):
        raise Exception('normally disabled')
    def closest(self,id):
        act = meta.Session.query(Activity).get(id)
        return unicode(act)
    def lonlat(self,id=None):
        cities = meta.Session.query(City)
        if id:
            cities=cities.filter_by(id=id)
        else:
            from sqlalchemy import or_
            cities = cities.filter(or_(City.lon==None,City.lat==None,City.extent_top==None))

        cities = cities.all()
        rt=''
        for ct in cities:
            lonlat = search_city(ct.name.encode('utf8'))
            if lonlat['successful'] and lonlat['result']:
                ct.lon = lonlat['result']['center']['lon']
                ct.lat = lonlat['result']['center']['lat']            
                ct.extent_top = lonlat['result']['extent']['top']
                ct.extent_bottom = lonlat['result']['extent']['bottom']
                ct.extent_left = lonlat['result']['extent']['left']
                ct.extent_right = lonlat['result']['extent']['right']
                meta.Session.commit()
            else:
                rt+="cannot get loc result for town '%s' - %s\n"%(ct.name,lonlat['reason'])
        c.output=rt
        return render('/parse_towns.html')
    def index(self):
        from pylons import config
        import os,re
        rg = re.compile('^(?P<id>[0-9]*) \t(?P<city_name>[^\t]*)\t(?P<mahoz>[^\t]*)\t(?P<population>[0-9,]*)')
        rt=''
        fname = os.path.join(config['pylons.paths']['root'],'towns.txt')
        rt+='reading from %s\n'%fname
        f = open(fname)
        for line in f:
            res = rg.search(line)
            if not res:
                rt+='cannot parse "%s"\n'%line
                continue
            ct = City()
            ct.name=res.group('city_name').strip()
            if meta.Session.query(City).filter_by(name=ct.name).all():
                rt+='city %s ALREADY EXISTS! skipping\n'%ct.name
                continue
            ct.population = int(re.compile('([,]+)').sub('',res.group('population').strip()))
            if request.params.get('getlonlat'):
                lonlat = search_city(ct.name)
                if lonlat['successful']:
                    ct.lon = lonlat['result']['center']['lon']
                    ct.lat = lonlat['result']['center']['lat']
            meta.Session.add(ct)
            rt+='inserted city %s'%ct.name
        meta.Session.commit()
        c.output=rt
        return render('/parse_towns.html')
