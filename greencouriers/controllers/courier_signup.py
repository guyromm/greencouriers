# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Area
from sqlalchemy import desc

log = logging.getLogger(__name__)
from greencouriers.controllers.signup import SignupController
from pylons.i18n.translation import _

class CourierSignupController(SignupController):
    def add_extra_fields(self,act):
        for fn in ['description','phone','delivery_price']:
            setattr(act,fn,self.form_result[fn])
            
    def getdata(self):
        c.areas = meta.Session.query(Area).filter_by(user_id=c.user_id,area_type='area').order_by(desc("id")).all()
    def __before__(self):
        c.hidden_inputs = ['poly_data']
        c.existings = ['existing_area']
        c.title=_(u'הרשמה לשליחים')
        #raise Exception(_(u'קיים'))
        return SignupController.__before__(self)
    tpl_postfix='courier'
    activity_type='courier'
