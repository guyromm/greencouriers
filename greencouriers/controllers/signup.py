# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
#from greencouriers import model
from greencouriers.model import Area,AreaPoint,Activity,Schedule,ScheduleHour,ScheduleWeekday,User,meta

log = logging.getLogger(__name__)

import re
preg = re.compile('([0-9\.]+), ([0-9\.]+)',re.MULTILINE)

import formencode,pprint
from pylons.decorators import validate
from formencode.variabledecode import NestedVariables

from pylons.i18n.translation import _,ungettext,set_lang,get_lang

#formencode.api.set_stdtranslation(domain="FormEncode", languages=[get_lang()])

from pylons.decorators.cache import beaker_cache
from sqlalchemy import desc


from sqlalchemy.orm.exc import NoResultFound

from pylons.i18n.translation import _

from weberror import collector
collector.FALLBACK_ENCODING = 'utf-8'

class AreaGiven(formencode.FancyValidator):
    def _to_python(self,value,state):
        try:
            ival = int(value.get('existing_area',0))
        except ValueError:
            ival=0
        polydata = value['poly_data']
        #raise Exception('fucking here %s - %s'%(polydata,value))
        if state.inserted_area:
            pass
        elif polydata and len(polydata) and polydata!='null':
            from shapely.geos import TopologicalError
            try:
                state.inserted_area = ins_loc(data=polydata,return_obj=True)
            except TopologicalError:
                meta.Session.rollback()
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'תיחום לא חוקי')})
            except ValueError:
                meta.Session.rollback()
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'תיחום לא חוקי')})
            msg='inserting location %s'%state.inserted_area;            log.info(msg)
            #raise Exception(msg)
            value['existing_area_id']=value['existing_area']=state.inserted_area.id

        elif ival:
            obj = meta.Session.query(Area).filter_by(id=ival).one()
            if not obj:
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'לא נמצא תחיום %d'%(ival))})
            if obj.user_id != state.user_id:
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'בעיית הרשאה בתיחום הנבחר!')})
            state.existing_area = obj
        else:
            raise formencode.Invalid(None,value,state,error_dict={'location':_(u'לא תיחמת איזור פעילות')})
        #raise Exception('giving back value %s'%value)
        return value

class ValidSchedule(formencode.FancyValidator):
    def parse_time(self,tmstr):
        import re,datetime
        res1 = re.compile('^([0-9]+)$').search(tmstr)
        if res1: 
            hour=int(res1.group(1))
            if hour==24:
                hour=23
                min=59
            else:
                min=0
            return datetime.time(hour,min)
        res2 = re.compile('^([0-9]+)\:([0-9]+)$').search(tmstr)
        if res2: 
            hour=int(res2.group(1))
            if hour==24:
                hour=23
                minute=59
            else:
                minute=int(res2.group(2))
            return datetime.time(hour,minute)
    def _to_python(self,value,state):
        #raise Exception('%s'%value)
        import time
        c.schedules_amt = len(value)

        oschedules=[]
        for val in value:
            val['h']['fr'] = h_fr = self.parse_time(val['h']['fr'])
            val['h']['to'] = h_to = self.parse_time(val['h']['to'])
            
            if not h_fr: raise formencode.Invalid(_(u'שעה תחתונה לא חוקית - %s')%val['h']['fr'],value,state)
            if not h_to: raise formencode.Invalid(_(u'שעה עליוה חוקית - %s')%val['h']['to'],value,state)
            if h_to<=h_fr: raise formencode.Invalid(_(u'טווח שעות אינו חוקי'),val,state)
            try:
                for d in val['d']: 
                    if int(d) not in range(1,8): raise formencode.Invalid(_(u'יום אינו חוקי %s')%d,value,state)
            except KeyError:
                raise formencode.Invalid(_(u'לא בחרת אף יום'),value,state)

            #check if schedule crosses with other schedules for this
            sc = Schedule()
            myweekdays=[]
            for dn in val['d']:
                myweekdays.append(ScheduleWeekday())
                myweekdays[-1].weekday = int(dn)
            sc.weekdays = myweekdays
            hr = ScheduleHour()
            hr.time_from = h_fr
            hr.time_to = h_to
            sc.hours = [hr]

            for sc2 in oschedules:
                if sc.overlaps(sc2):
                    state.schedule_valid=False
                    raise formencode.Invalid(_(u'שעות אלו כבר תפוסות בלו"ז שלך.'),value,state)
            oschedules.append(sc)

            #raise Exception('%s'%val)
            state.schedule_valid=True
        return value
class ILPhoneNumber(formencode.validators.FancyValidator):
    def _to_python(self,value,state):
        import re

        rg = re.compile('^(0[0-9]{1,2})(\-| |)([0-9]{7,7})$')
        rg2 = re.compile('^1(\-| |)(7|8)00(.*)$')
        rg2repl = re.compile('([^0-9]+)')
        res = rg.search(value)
        if res:
            prefix = res.group(1)
            number = res.group(3)
            return '%s-%s'%(prefix,number)
        elif rg2.search(value):
            res2 = rg2.search(value)
            prefix = res2.group(2)
            number = rg2repl.sub('',res2.group(3))
            if len(number)!=6:
                raise formencode.Invalid(_(u'number is bad length (must be 6)'),value,state)
            return '1-%s00-%s'%(prefix,number)
#            raise Exception('got num %s'%number)
        else:    
            raise formencode.Invalid(_(u'המספר לא מתאים לפורמט ##(#)-#######'),value,state)

        
class CourierSignup(formencode.Schema):
    pre_validators = [NestedVariables(),AreaGiven()]
    #hours = ValidHours(not_empty=True)
    #days = ValidDays(not_empty=True)
    schedule = ValidSchedule(not_empty=True)
    #description = formencode.validators.UnicodeString(not_empty=True)
    phone = ILPhoneNumber(not_empty=True)
    delivery_price = formencode.validators.Number(not_empty=True,min=5,max=100)
    allow_extra_fields=True

#weekdays = {1:_(u'א\''),2:_(u'ב\''),3:u(u'ג\''),4:_(u'ד\''),5:_(u'ה\''),6:_(u'ו\''),7:_(u'ש\'')}
weekdays = {1:u'א',2:u'ב',3:u'ג',4:u'ד',5:u'ה',6:u'ו',7:u'ש'}

def parse_polydata(dt):
    res = preg.findall(dt)
    return res

def get_area(id=None,a=None):
    if not a:
        if not id: raise Exception('no id or obj given')
        a = meta.Session.query(Area).get(id)
    if a.user_id!=c.user_id: raise Exception('bad permission for area')
    import simplejson
    return simplejson.dumps({'result':'success'
                             ,'area':{'id':a.id,'label':a.label}
                             ,'points':[{'id':p.id,'lat':p.pos_lat,'lon':p.pos_lon} for p in a.points]
                             })        
#times={}
def ins_loc(data=None,return_obj=False,area_type='area'):
    #if area_type not in times: times[area_type]=0
    #times[area_type]+=1
    #logline='inserting %s, data %s - return obj = %s, time %d'%(area_type,data,return_obj,times[area_type])
    #log.debug(logline)
    #if times[area_type]>1: raise Exception(logline)

    if not data:
        coords = parse_polydata(request.params.get('coords'))
    else:
        coords = parse_polydata(data)

    #make sure that poly is valid - 
    if area_type=='area':
        from shapely.geometry import Polygon
        poly = Polygon([(float(p[0]),float(p[1])) for p in coords])
        poly.centroid
        poly.area
        poly.union(Polygon([(5,5),(5.5,5),(5.5,6)]))
        if len(coords)==4 and coords[1]==coords[2] and coords[0]==coords[3]:
            from shapely.geos import TopologicalError
            raise TopologicalError('its not a polygon but a line!')
        #raise Exception('area %s, centroid %s'%(poly.area,poly.centroid))
    
    a = Area()
    if not c.user_id: raise Exception('no user in ins_loc!')
    a.user_id = c.user_id
    a.area_type=unicode(area_type)
    meta.Session.add(a)
    #meta.Session.commit()
    for coord in coords:
        cobj = AreaPoint()
        #cobj.area_id = a.id
        cobj.area = a
        cobj.pos_lon = coord[0]
        cobj.pos_lat = coord[1]
        meta.Session.add(cobj)

    meta.Session.commit()
    if return_obj:
        return a
    return get_area(a=a)

def search_country_google(cc):
    fns = ['lon','lat','north','south','east','west']
    import urllib
    from greencouriers.model import Country
    if cc=='a2': cc='il'
    try:
        co = meta.Session.query(Country).filter_by(iso=cc.upper()).one()
    except:
        raise Exception('cannot find your country, %s'%cc.upper())
    if co.lon:
        resp = {}
        for fn in fns:
            resp[fn]=getattr(co,fn)
        return resp

    params = urllib.urlencode({'q':co.name,'key':config['global_conf']['google_maps_api'],'sensor':'false','output':'json','oe':'utf8'})
    murl = 'http://maps.google.com/maps/geo?%s'%params
    f = urllib.urlopen(murl)
    import simplejson
    resp = simplejson.load(f)
    if 'Placemark' in resp:
        co.lon = resp['Placemark'][0]['Point']['coordinates'][0]
        co.lat = resp['Placemark'][0]['Point']['coordinates'][1]
        co.west = resp['Placemark'][0]['ExtendedData']['LatLonBox']['west']
        co.east = resp['Placemark'][0]['ExtendedData']['LatLonBox']['east']
        co.north = resp['Placemark'][0]['ExtendedData']['LatLonBox']['north']
        co.south = resp['Placemark'][0]['ExtendedData']['LatLonBox']['south']
        meta.Session.commit()
        return search_country_google(cc)
    else:
        return False

def search_city_google(city_name,country,street=None):
    log.info('%s , %s, %s'%(country,city_name,street))
    import urllib
    if street:
        #qry=u'%s, %s'%(street.encode('utf8'),city_name.encode('utf8'))
        qry = unicode(street)+u', '+unicode(city_name)
        qry=qry.encode('utf8')
    else:
        qry=city_name
    params = urllib.urlencode({'q':qry,'key':config['global_conf']['google_maps_api'],'sensor':'false','output':'json','oe':'utf8','gl':country})
    murl = 'http://maps.google.com/maps/geo?%s'%params
    f = urllib.urlopen(murl)
    import simplejson
    resp = simplejson.load(f)
    #raise Exception(resp)
    if resp['Status']['code']==200:
        lon = resp['Placemark'][0]['Point']['coordinates'][0]
        lat = resp['Placemark'][0]['Point']['coordinates'][1]
        west = resp['Placemark'][0]['ExtendedData']['LatLonBox']['west']
        robj = {'result':{'center':{'lon':lon,'lat':lat}
                          ,'extent':{'top':resp['Placemark'][0]['ExtendedData']['LatLonBox']['north']
                                    ,'bottom':resp['Placemark'][0]['ExtendedData']['LatLonBox']['south']
                                    ,'left':resp['Placemark'][0]['ExtendedData']['LatLonBox']['west']
                                    ,'right':resp['Placemark'][0]['ExtendedData']['LatLonBox']['east']
                                    }
                          }
                ,'successful':True
                }
    else: 
        robj = {'successful':False}
    if street:
        return search_street(city_name,street,country,robj)
    else:
        return search_city(city_name,country,robj)

def search_street(city_name,street_name,country,insdata=None):
    if not insdata and country!='il':
        return search_city_google(city_name,country,street_name)
    if not insdata:
        import urllib
        params = urllib.urlencode({'street_name':street_name.encode('utf8'),'city_name':city_name.encode('utf8')}) #,'street_name':u'מכבי'.encode('utf8')})
        murl = 'http://www.waze.co.il/WAS/search?%s'%params
        f = urllib.urlopen(murl)
        import simplejson
        fstr=f.read()
        resp = simplejson.loads(fstr)

    else:
        resp = insdata
    try:
        if resp['successful']:
            from greencouriers.model import City,Street
            #find city
            ct = meta.Session.query(City).filter_by(name=city_name,country=country).one()
            if ct:
                try:
                    to_create=False
                    st = meta.Session.query(Street).filter_by(city=ct,name=street_name).one()
                except NoResultFound:
                    st = Street()
                    st.name = street_name
                    st.city=ct
                    st.country=country
                    to_create=True
                st.lon = resp['result']['center']['lon']
                st.lat = resp['result']['center']['lat']
                st.extent_top = resp['result']['extent']['top']
                st.extent_bottom = resp['result']['extent']['bottom']
                st.extent_left = resp['result']['extent']['left']
                st.extent_right = resp['result']['extent']['right']
                if to_create:
                    if not st.country: raise Exception('country unset in street')
                    meta.Session.add(st) 
                meta.Session.commit()
    except ValueError:
        import re
        if re.compile('HTTP Status 500').search(fstr):
            return simplejson.dumps({'succesful':False,'reason':'remote server returned 500'})
        raise Exception('unexpected response from server')
    return resp
def search_city(city_name,country,insdata=None):
    if not insdata and country!='il':
        return search_city_google(city_name,country)
    if not insdata:
        import urllib
        params = urllib.urlencode({'city_name':city_name}) #,'street_name':u'מכבי'.encode('utf8')})
        murl = 'http://www.waze.co.il/WAS/search?%s'%params
        f = urllib.urlopen(murl)
        import simplejson
        resp = simplejson.load(f)
    else:
        resp = insdata

    if resp['successful']:
        from greencouriers.model import City,meta
        commit=False
        qres=meta.Session.query(City).filter_by(name=city_name,country=country).all()
        if qres:
            ct = qres[0]
        else: 
            ct = City()
            ct.country=country
            ct.name = city_name
            meta.Session.add(ct)
            commit=True
        if ct and not ct.lon:
            ct.lon = resp['result']['center']['lon']
            ct.lat = resp['result']['center']['lat']
            ct.extent_top=resp['result']['extent']['top']
            ct.extent_bottom=resp['result']['extent']['bottom']
            ct.extent_right=resp['result']['extent']['right']
            ct.extent_left=resp['result']['extent']['left']
            ct.population=-1
            commit=True
        if commit:meta.Session.commit()
    return resp

from facebook.wsgi import facebook
from decorator import decorator

@decorator
def force_login(f,*args,**kws):
    auth = False
    if 'greenie_auth' in session and session['greenie_auth']:
        try:
            u = meta.Session.query(User).filter_by(login_hash=session['greenie_auth']).one()
            #FIXME: we don't handle a case here in which the user has a previous facebook account and he attempts to associate it to a second email account..
            if not u.fb_uid and facebook.check_session() and not len(meta.Session.query(User).filter_by(fb_uid=facebook.uid).all()):
                u.fb_uid=facebook.uid
                meta.Session.commit()
            c.user = u
            c.user_id = u.id
            auth=True
        except:
            #pass
            raise

            
    if config['use_facebook']!='true': 
        c.use_facebook=False
# we have an alternative auth system in place now.
#         u  = meta.Session.query(User).get(1)
#         if not u:
#             u = User()
#             u.id = 1
#             u.fb_uid='12341234'
#             u.name='Test user'
#             meta.Session.add(u); meta.Session.commit()
#         c.user = u
#         c.user_id = u.id
#        return f(*args,**kws)
    c.use_facebook=True
    action = request.environ['pylons.routes_dict']['action']
    login_action='fb_login'
    fbses = facebook.check_session()
    if fbses:
        if not facebook.uid: raise Exception('no fb uid!')
        #raise Exception('fb uid:%s'%facebook.uid)
        try:
            u = meta.Session.query(User).filter_by(fb_uid=facebook.uid).one()
        except NoResultFound:
            u = User()
            u.fb_uid = facebook.uid
            u.name = facebook.users.getInfo(facebook.uid)[0]['name']
            #facebook.users.setStatus("just registered on <a href='http://www.greenie.co.il'>Green Couriers</a> - the green way of delivering.",False)
            #facebook.feed.publishUserAction(51359366316)
            from greencouriers.controllers.auth import default_user_attrs
            default_user_attrs(u,request)
            meta.Session.add(u); meta.Session.commit()
        c.user_id=u.id
        c.user = u
        auth = True
    elif not auth:
        if action!=login_action:
            # we could not login. see if there are any last exceptions?
            if request.urlvars['controller']=='main' or \
                    (request.urlvars['action'] in ['login','signup','logout',_('reset')]\
                    and not re.compile(_('_signup$')).search(request.urlvars['controller'])):
                return f(*args,**kws)
            # redirect to login.
            return redirect(url.current(action=login_action,return_action=action))
    if auth==True:
        if c.user:
            from greencouriers.lib.base import freemap_url_from_country
            c.use_google_maps,c.freemap_url = freemap_url_from_country(c.user.country,c.user)
            #if c.use_google_maps: raise Exception('country of user %s is %s'%(c.user.id,c.user.country))
            #raise Exception('extracted %s,%s from %s'%(c.use_google_maps,c.freemap_url,c.user.country))
        return f(*args,**kws)

class SignupController(BaseController):
    weekdays = None

    update_mode=False
    activity_type='none'
    @force_login
    def __before__(self):
        self.weekdays = {1:_(u'א'),2:_(u'ב'),3:_(u'ג'),4:_(u'ד'),5:_(u'ה'),6:_(u'ו'),7:_(u'ש')}
        #raise Exception(get_lang())
        formencode.api.set_stdtranslation(domain="FormEncode", languages=get_lang())
        c.weekdays = weekdays
        c.existings = ['existing_area']
        c.existings_labels={'existing_area':_(u'תיחום'),'existing_marker':_(u'בית עסק')}
        c.activity_type=type(self).activity_type
        c.submit_button=_(u'הירשם')
        pass
    def fb_login(self):
        return render('/fb_login.html')
    def __init__(self):
        return BaseController.__init__(self)
    def transtest(self):
        set_lang('he')
        return _('Missing value')
    def delete(self,id):
        act = meta.Session.query(Activity).get(id)
        if act.user_id!=c.user_id: raise Exception('wrong user!')
        meta.Session.delete(act) ; meta.Session.commit()
        return redirect(url.current(controller='my_account',action='index',id=None))
    def index(self):
        self.getdata()
        for en in c.existings:
            singular = re.sub('^existing_','',en)
            inserted = re.sub('^existing_','inserted_',en)
            plural = singular+'s'
            if not getattr(c,en+'_id'): setattr(c,en+'_id',None)
            if len(getattr(c,plural)):
                setattr(c,'start_marking_'+singular,False)
                if not getattr(c,en):
                    setattr(c,en,getattr(c,plural)[0])
                    setattr(c,en+'_id',getattr(c,plural)[0].id)
            else:
                setattr(c,'start_marking_'+singular,True)
                setattr(c,en,None)
            #raise Exception('checking for c.%s - %s'%(inserted,getattr(c,inserted)))
            if getattr(c,inserted):
                #raise Exception('setting existing to val of inserted. plus ive got %s'%len(getattr(c,plural)))
                setattr(c,en+'_id',getattr(c,inserted).id)
                setattr(c,en,getattr(c,inserted))

        if not type(self).update_mode:  c.act = Activity()
        #raise Exception('existing area_id is %s'%c.existing_area_id)
        #assume a2 is israel
        if c.user.country<>['il','a2']:
            c.initial_coords=search_country_google(c.user.country)
            #raise Exception('got %s for %s'%(c.initial_coords,c.user.country))
        rt= render('/%s_signup.html'%type(self).tpl_postfix)
        return rt
    @validate(schema=CourierSignup(),form='index',post_only=False,on_get=True,state=c)
    def signup(self,id=None):
        return self.noval_signup(id)

    def noval_signup(self,id=None):
        log.info('in signup method')
        poly_data = request.params.get('poly_data')
        existing_area = request.params.get('existing_area')
        existing_marker = request.params.get('existing_marker')
        
        if type(self).update_mode:
            #raise Exception('getting activity %s , %s'%(id,request.params))
            act = meta.Session.query(Activity).get(id)
            if not act.user_id==c.user_id: raise Exception('security violation trying to update someone elses shite')
        else:
            act = Activity()
        act.user = meta.Session.query(User).get(c.user_id)
        act.activity_type=type(self).activity_type
        #raise Exception('act user is %s'%act.user)
        if c.inserted_area:
            act.area = a = c.inserted_area
        elif existing_area:
            log.info('about to commit - existing area is %s'%existing_area)
            act.area_id = existing_area
        elif act.activity_type=='courier':
            raise Exception('no area set to be inserted with this activity!')
        if c.inserted_marker:
            act.marker = im = c.inserted_marker
        elif existing_marker:
            #act.marker = im = meta.Session.query(Area).get(existing_marker)
            act.marker_id = existing_marker
        elif act.activity_type=='business':
            raise Exception('no location set to be inserted with this activity')


        #raise Exception('about to insert activity with area %s (area_id %s) , user %s and activity type "%s"'%(act.area,act.area_id,act.user,act.activity_type))
        self.add_extra_fields(act)

        if type(self).update_mode: 
            [meta.Session.delete(sch) for sch in act.schedules]
        else:
            meta.Session.add(act)
        meta.Session.commit()
        if 'schedule' in self.form_result:
            for sch in self.form_result['schedule']:
                scho = Schedule()
                scho.activity = act
                meta.Session.add(scho)
                sch_h = ScheduleHour()
                sch_h.schedule = scho
                sch_h.time_from = (sch['h']['fr'])
                #raise Exception(type(sch['h']['fr']))
                sch_h.time_to = (sch['h']['to'])
                meta.Session.add(sch_h)
                for dn in sch['d']:
                    sch_d = ScheduleWeekday()
                    sch_d.schedule = scho
                    sch_d.weekday = dn
                    meta.Session.add(sch_d)
        
        meta.Session.commit()
        if type(self).update_mode:
            return redirect(url.current(controller=act.activity_type,id=act.id,justadded=False))
        else:
            return redirect(url.current(controller=act.activity_type,action='matches_map',id=act.id,justadded=True))
        #    return render('/%s_signup-complete.html'%type(self).tpl_postfix)
    def get_area(self,id=None,a=None):
        return get_area(id=id,a=a)
    def ins_loc(self,data=None,return_obj=False,area_type='area'):
        return ins_loc(data=data,return_obj=return_obj,area_type=area_type)
    #http://www.waze.co.il/WAS/autocomplete?q=%D7%9E%D7%9B%D7%91&limit=10&name=street_name&city_name=%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+-+%D7%99%D7%A4%D7%95
    #@beaker_cache()
    def street_autocomplete(self,city_name,street_name):
        output='street_autocomplete(%s,%s)'%(city_name,street_name)
        log.info(output) 
        #raise Exception(output)
        import urllib
        params = urllib.urlencode({'q':street_name.encode('utf8'),'limit':10,'name':'street_name','city_name':city_name.encode('utf8')})
        url = 'http://www.waze.co.il/WAS/autocomplete?%s'%params
        f = urllib.urlopen(url)
        results = f.read().strip().split("\n")
        from greencouriers.model import City,Street
        try:
            ct = meta.Session.query(City).filter_by(name=city_name).one()
        except NoResultFound:
            ct=None
        import simplejson
        if ct:
            for sres in results:
                street_name = sres.strip()
                if not street_name: continue
                if not meta.Session.query(Street).filter_by(city=ct,name=street_name).all():
                    st = Street()
                    st.city=ct
                    st.name = street_name
                    import pylons

                    st.country = config['global_conf']['default_country'].lower()
                    #raise Exception('setting country to %s'%st.country)
                    meta.Session.add(st); meta.Session.commit()
            #response.headers['content-type']='application/json'
        return simplejson.dumps({'results':[{'id':res,'value':res} for res in results]})
    #http://www.waze.co.il/WAS/autocomplete?q=%D7%AA%D7%9C&limit=10&name=city_name
    #@beaker_cache()
    def city_autocomplete(self,city_name):
        import urllib
        params = urllib.urlencode({'q':city_name.encode('utf8'),'limit':10,'name':'city_name'})
        url = 'http://www.waze.co.il/WAS/autocomplete?%s'%params
        f = urllib.urlopen(url)
        fstr = f.read()
        results = fstr.strip().split("\n")
        #just for client debugging
        #if 'REFERER' not in request.headers:return fstr
        from greencouriers.model import City,meta
        for res_name in results:
            if not res_name.strip(): continue
            ctres = meta.Session.query(City).filter_by(name=res_name.strip()).all()
            if not ctres:
                ct = City()
                ct.name = res_name.strip()
                ct.population=-1
                import pylons
                ct.country = config['global_conf']['default_country'].lower()

                meta.Session.add(ct) ; 
        meta.Session.commit()
        import simplejson
        #response.headers['content-type']='application/json'
        return simplejson.dumps({'results':[{'id':res,'value':res} for res in results]
                                 ,'for':city_name})
    #@beaker_cache()
    def search_city(self,city_name):
        city_name = city_name.encode('utf8')
        if c.user.country: 
            country=c.user.country.lower()
        else:
            country=config['global_conf']['default_country'].lower()
        resp = search_city_google(city_name=city_name,country=country)
        response.headers['content-type']='application/json'
        import simplejson
        return simplejson.dumps(resp)
    #@beaker_cache()
    def search_street(self,city_name,street_name):
        city_name = city_name #.encode('utf8')
        if c.user.country: 
            country=c.user.country.lower()
        else:
            country=config['global_conf']['default_country'].lower()
        import simplejson
        response.headers['content-type']='application/json'
        #raise Exception('invoking search street with city:%s(%s),street:%s(%s),country:%s(%s)'%(city_name,type(city_name),street_name,type(street_name),country,type(country)))
        return simplejson.dumps(search_city_google(city_name,street=street_name,country=country))

