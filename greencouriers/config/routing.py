"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
#from pylons import config
from routes import Mapper

class LanguageDetectingMapper(Mapper):
    def match(self, url):
        nurl, lang = self.detect_language(url)
        rt= Mapper.match(self,nurl)
        if rt!=None:
            rt[0]['_lang']=lang
        return rt
        #raise Exception('url is %s, lang is %s'%(url,lang))
        #raise Exception('res: %s'%result)
#         try:
#             result[0]
#             #raise Exception('standard %s'%result[0])
#         except KeyError,e:
#             #raise Exception('nonstandard result %s'%result[0])
#             pass

        if result[0]:
            result[0]['_lang'] = lang
        if self.debug:
            return result[0], result[1], result[2]
        if result[0]:
            raise Exception('am here biatch')
            return result[0]
        #raise Exception('dead here')
        return None
    def routematch(self, url):
        nurl,lang = self.detect_language(url)
        rt= Mapper.routematch(self,nurl)
        if rt:
            rt[0]['_lang']=lang
        return rt

    def detect_language(self, url):
        # Detect and return the language code, if
        import re
        rg = re.compile('^/(en|he)/(.*)$')
        res = rg.search(url)
        if res:
            return ('/'+res.group(2),res.group(1))
        else:
            return (url,'he')
            #raise Exception('detecting language in %s got %s'%(url,res.group(1)))
        
    # any, and return the URL without it.

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = LanguageDetectingMapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    
    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    from greencouriers.controllers.admin import AdminController
    
    #cancelled by milez 2011-1-19
    #from formalchemy.ext.pylons import maps
    #maps.admin_map(map, AdminController, 'admin')    

    deflang='he'
    langs = ['he','en']
    for ln in langs:
        if deflang==ln:
            prefix=''
        else:
            prefix='/{_lang:%s}'%ln
        map.connect(prefix+'/',controller='main',action='index',_lang=ln)
        map.connect(prefix+'/{controller}/',action='index',_lang=ln)
        map.connect(prefix+'/{controller}/{id:([0-9]+)}/',action='index',_lang=ln)
        map.connect(prefix+'/{controller}/{action:search_city}/{city_name}/',_lang=ln)
        map.connect(prefix+'/{controller}/{action:search_street}/{city_name}/{street_name}/',_lang=ln)
        map.connect(prefix+'/{controller}/{action:city_autocomplete}/{city_name}/',_lang=ln)
        map.connect(prefix+'/{controller}/{action:street_autocomplete}/{city_name}/{street_name}/',_lang=ln)
        map.connect(prefix+'/{controller}/{action}',_lang=ln)
        map.connect(prefix+'/{controller}/{action}/{id}',_lang=ln)
        map.connect(prefix+'/{controller:schedule_intersections}/{id}/{tid}/',action='index',_lang=ln)

    return map
