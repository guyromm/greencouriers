import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render

from greencouriers.model import meta,Activity,City,Street
import re

log = logging.getLogger(__name__)

class MyDataGrid(object):
    fields=[]
    field_labels={}
    exclude_fields=[]
    exclude_relationship_fields=False
    def __init__(self):
        self.query = meta.Session.query(self.model)
        if not self.fields: 
            self.fields = getdefaultfields(self.fields)
    def render(self):
        self.query_res = self.query.all()
        c.dg = self
        return render('/data_grid.html')

_goodfield = re.compile('^([a-z]+)',re.IGNORECASE)
_badfield = re.compile('_id$')

def goodfield(fn):
#    if fn in self.exclude_fields: return False
    if not _goodfield.search(fn): return False
    if _badfield.search(fn): return False
    return True
def getdefaultfields(model):
    fields=[];
    for fn in dir(model):
        if goodfield(fn):
            fields.append((fn.capitalize(),fn))
    return fields

class ActivitiesTable(MyDataGrid):
    model = Activity
    exclude_relationship_fields=True
    exclude_fields = ['id','activity_types','max_delivery_time']

class ActivitiesAdminController(BaseController):
    def __before__(self):
        raise Exception('TODO')
    def testicle(self):
        m = Activity()
        raise Exception('%s'%m)
    def index(self):
        c.activities_table = ActivitiesTable()
        return render('/activities_admin.html')
