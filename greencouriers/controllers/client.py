# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import ClientMatch,CourierMatch,meta,Activity
log = logging.getLogger(__name__)

from greencouriers.controllers.business import BusinessController

class ClientController(BusinessController):
    activity_type='client'
    match_type=ClientMatch
    show_sched=False
    def matches_map(self,id):
        self.load_matches(id)
        act = meta.Session.query(Activity).get(id)
        c.act = act
        c.activities = [cm.activity for cm in c.service_matches]
        included=[]
        for sm in c.activities:
            matches = meta.Session.query(CourierMatch).filter_by(src=sm.id).all()
            for mt in matches:
                mt.activity = meta.Session.query(Activity).get(mt.tgt)
                if not mt.activity in included:
                    c.service_matches+=[mt]
                    included.append(mt.activity)
        c.activities+=included
        c.title=u'התאמות שירות ל%s'%act
        self.justadded(c.act)
        return render('/%s_matches_map.html'%act.activity_type)
