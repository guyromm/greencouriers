# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Activity

log = logging.getLogger(__name__)
from greencouriers.controllers.courier_signup import CourierSignupController
from pylons.i18n.translation import _

class CourierEditController(CourierSignupController):
    update_mode=True
    def index(self,id):
        self.act = meta.Session.query(Activity).get(id)
        if not self.act.user.id == c.user_id: raise Exception('security violation for activity %s , %s'%(self.act,c.user_id))
        self.existing_area = c.existing_area = self.act.area
        c.existing_area_id=c.existing_area.id
        #raise Exception('existing area %s'%self.existing_area.id)
        c.schedules_amt = len(self.act.schedules)
        c.schedules = self.act.schedules
        c.act = self.act
        c.no_accord=True
        c.title=_(u'עדכון פרטי פעילות')
        c.submit_button=_(u'עדכון')
        c.update_mode=True
        return CourierSignupController.index(self)
