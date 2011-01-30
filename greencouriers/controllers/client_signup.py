# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect
from greencouriers.model import meta,Area
from greencouriers.lib.base import BaseController, render

from greencouriers.controllers.signup import SignupController,CourierSignup,AreaGiven,ins_loc

from sqlalchemy import desc

log = logging.getLogger(__name__)

from greencouriers.controllers.signup import ILPhoneNumber,NestedVariables,formencode,validate
from greencouriers.controllers.business_signup import MarkerGiven
from pylons.i18n.translation import _

class ClientSignup(CourierSignup):
    pre_validators = [NestedVariables(),MarkerGiven()]
    address = formencode.validators.UnicodeString(not_empty=False)
    phone = ILPhoneNumber(not_empty=False)
    schedule=None
    delivery_price=None
class ClientSignupController(SignupController):
    def add_extra_fields(self,act):
        from greencouriers.controllers.courier_signup import CourierSignupController
        for fn in ['phone','address']:
            setattr(act,fn,self.form_result[fn])
    def getdata(self):
        c.markers = meta.Session.query(Area).filter_by(user_id=c.user_id,area_type='marker').order_by(desc("id")).all()
    def __before__(self):
        c.hidden_inputs = ['marker_data']
        rt= SignupController.__before__(self)

        c.existings = ['existing_marker']
        c.existings_labels={'existing_area':_(u'תיחום'),'existing_marker':_(u'מיקום לקוח')}
        c.title=_(u'הרשמה ללקוחות')
        c.submit_button=_(u'הירשם')
        return rt
    tpl_postfix='client'
    activity_type='client'
    @validate(schema=ClientSignup(),form='index',post_only=False,on_get=True,state=c)
    def signup(self,id=None):    
        return self.noval_signup(id)
