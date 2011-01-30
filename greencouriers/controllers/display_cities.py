import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,City

log = logging.getLogger(__name__)

class DisplayCitiesController(BaseController):

    def index(self):
        c.cities = meta.Session.query(City).filter(City.lon!=None).filter(City.lat!=None).all()
        return render('/display_cities.html')
