# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
#from greencouriers import model

log = logging.getLogger(__name__)

import re
preg = re.compile('([0-9\.]+), ([0-9\.]+)',re.MULTILINE)

class MaptestController(BaseController):
    def __before__(self):
        raise Exception('disabled')
    def index(self):
        c.pd = request.params.get('poly_data')
        if c.pd:
            parsed = self.parse_polydata(c.pd)
            import string
            c.autodraw_coords= '['+string.join(['new OpenLayers.Geometry.Point(%f,%f)'%(float(pdi[0]),float(pdi[1])) for pdi in parsed],',')+']'

        return render('/maptest.html')
    def search_address(self,id):
        import urllib
        params = urllib.urlencode({'city_name':id.encode('utf8')}) #,'street_name':u'מכבי'.encode('utf8')})
        murl = 'http://www.waze.co.il/WAS/search?%s'%params
        #http://www.waze.co.il/WAS/search?city_name=%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+-+%D7%99%D7%A4%D7%95&street_name=
        f = urllib.urlopen(murl)
        import simplejson
        resp = simplejson.load(f)
        response.headers['content-type']='text/json'
        return simplejson.dumps(resp)
    def parse_polydata(self,dt):
        res = preg.findall(dt)
        return res
    
    
#correct
#http://www.waze.co.il/WAS/search?city_name=%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+-+%D7%99%D7%A4%D7%95&street_name=%D7%9E%D7%9B%D7%91%D7%99
#2
#http://www.waze.co.il/WAS/search?city_name=%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+-+%D7%99%D7%A4%D7%95&street_name=%D7%9E%D7%9B%D7%91%D7%99
#wrong
#http://www.waze.co.il/WAS/search?city_name=%FA%EC+%E0%E1%E9%E1+-+%E9%F4%E5&street_name=%EE%EB%E1%E9
