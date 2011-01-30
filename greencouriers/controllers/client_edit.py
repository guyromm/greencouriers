# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import Activity,meta

log = logging.getLogger(__name__)

from greencouriers.controllers.client_signup import ClientSignupController

class ClientEditController(ClientSignupController):
    update_mode=True
    def index(self,id):
        self.act = meta.Session.query(Activity).get(id)
        if not self.act.user.id == c.user_id: raise Exception('security violation for activity %s , %s != %s'%(self.act.id,c.user_id,self.act.user_id))
        self.existing_marker = c.existing_marker = self.act.marker
        c.existing_marker_id=c.existing_marker.id
        c.act = self.act
        c.no_accord=True
        c.title=u'עדכון פרטי לקוח'
        c.submit_button=u'עדכן'
        c.update_mode=True
        return ClientSignupController.index(self)
