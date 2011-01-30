# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Activity,CourierMatch

log = logging.getLogger(__name__)

from greencouriers.controllers.business import BusinessController

class CourierController(BusinessController):
    activity_type='courier'
    match_type=CourierMatch
