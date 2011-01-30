# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import Activity,meta

log = logging.getLogger(__name__)

from greencouriers.controllers.business_signup import BusinessSignupController

class BusinessEditController(BusinessSignupController):
    update_mode=True
    def index(self,id):
        self.act = meta.Session.query(Activity).get(id)
        if not self.act: abort(404)
        if not self.act.user.id == c.user_id: raise Exception('security violation for activity %s , %s'%(self.act,c.user_id))
        self.existing_marker = c.existing_marker = self.act.marker
        c.existing_marker_id=c.existing_marker.id
        c.schedules_amt = len(self.act.schedules)
        c.schedules = self.act.schedules
        c.act = self.act
        c.no_accord=True
        c.title=u'עדכון פרטי פעילות'
        c.submit_button=u'עדכון'
        c.update_mode=True
        return BusinessSignupController.index(self)
