"""The base Controller API

Provides the BaseController class for subclassing.
"""
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from greencouriers.model import meta

from pylons import tmpl_context as c
from pylons import config

def freemap_url_from_country(country_code,user=None):
    import os
    fname = os.path.join(config['pylons.paths']['static_files'],'js','freemap-%s.js'%country_code)
    if os.path.exists(fname):
        return (False,'/js/freemap-%s.js'%country_code)
    else:
        #raise Exception('could not find country %s belonging to %s'%(country_code,user))
        return (True,'/js/freemap-default.js')

class BaseController(WSGIController):
    
    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        from pylons.i18n.translation import set_lang
        set_lang(environ['pylons.routes_dict']['_lang'])
        
        #figure out which map to display based on geoloc
        from pygeoip import GeoIP
        gi = GeoIP('/usr/share/GeoIP/GeoIP.dat') #GeoIP.GEOIP_MEMORY_CACHE)
        country_code = gi.country_code_by_addr(str(environ['REMOTE_ADDR']))
        #raise Exception('%s from %s'%(country_code,environ['REMOTE_ADDR']))
        if not country_code or country_code.lower() in ['a2']: 
            country_code = config['global_conf']['default_country']
        country_code=country_code.lower()

        c.use_google_maps,c.freemap_url = freemap_url_from_country(country_code)


        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            meta.Session.remove()
        
