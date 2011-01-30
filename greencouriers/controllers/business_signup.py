# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Area
from sqlalchemy import desc

log = logging.getLogger(__name__)
import formencode
from greencouriers.controllers.signup import SignupController,CourierSignup,AreaGiven,ins_loc
from pylons.decorators import validate

from formencode.variabledecode import NestedVariables
from pylons.i18n.translation import _

class MarkerGiven(formencode.FancyValidator):
    def _to_python(self,value,state):
        try:
            ival = int(value.get('existing_marker',0))
        except ValueError:
            ival=0
        markerdata = value['marker_data']
        #raise Exception('fucking here %s - %d'%(polydata,ival))
        if state.inseretd_marker:
            pass
        elif markerdata and len(markerdata) and markerdata!='null':
            state.inserted_marker = ins_loc(data=markerdata,return_obj=True,area_type='marker')
            #raise Exception('just inserted marker %s'%state.inserted_marker)
        elif ival:
            obj = meta.Session.query(Area).filter_by(id=ival).one()
            if not obj:
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'לא נמצא מיקום בית עסק')})
            if obj.user_id != state.user_id:
                raise formencode.Invalid(None,ival,state,error_dict={'location':_(u'בעיית הרשאה במיקום הנבחר!')})
            state.existing_marker = obj
        else:
            raise formencode.Invalid(None,value,state,error_dict={'location':_(u'לא סימנת מקום בית עסק')})
        return value

deliveries_freq = [('rare',_(u'לעיתים רחוקות')),('occasional',_(u'לעיתים מזדמנות')),('frequent',_(u'לעיתים קרובות'))] 
#validation schema
class BusinessSignup(CourierSignup):
    pre_validators = [NestedVariables(),MarkerGiven()]
    url = formencode.validators.URL(not_empty=False)
    business_name = formencode.validators.UnicodeString(not_empty=True)
    max_delivery_time = formencode.validators.Number(not_empty=True)
    deliveries_freq = formencode.validators.OneOf(['rare','occasional','frequent'])
    delivery_price = None
    
class BusinessSignupController(SignupController):
    def add_extra_fields(self,act):
        from greencouriers.controllers.courier_signup import CourierSignupController
        for fn in ['business_name','description','phone','url','max_delivery_time','deliveries_freq']:
            setattr(act,fn,self.form_result[fn])
    def getdata(self):
        c.markers = meta.Session.query(Area).filter_by(user_id=c.user_id,area_type='marker').order_by(desc("id")).all()
    def __before__(self):
        c.hidden_inputs = ['marker_data']
        rt= SignupController.__before__(self)
        c.existings = ['existing_marker']
        c.existings_labels={'existing_area':_(u'תיחום'),'existing_marker':_(u'בית עסק')}
        c.title=_(u'הרשמה לבתי עסק')
        c.submit_button=_(u'הירשם')
        return rt
    tpl_postfix='business'
    activity_type='business'

    @validate(schema=BusinessSignup(),form='index',post_only=False,on_get=True,state=c)
    def signup(self,id=None):    
        return self.noval_signup(id)


