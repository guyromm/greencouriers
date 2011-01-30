import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
#from greencouriers import model

log = logging.getLogger(__name__)

class HelpController(BaseController):
    def marking(self):
        return render('/help_marking.html')
    def index(self):
        # Return a rendered template
        #   return render('/template.mako')
        # or, Return a response
        return 'Hello World'
