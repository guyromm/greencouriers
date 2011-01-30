import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Schedule,ScheduleIntersectionResult

log = logging.getLogger(__name__)

class ScheduleIntersectionsController(BaseController):
    def index(self,id=None,tid=None):
        response.headers['contenent-type']='text/plain'
        s1s = meta.Session.query(Schedule)
        if id:
            s1s = s1s.filter_by(id=id)
        s1s = s1s.all()
        
        yield "got %d schedules to check<br />"%len(s1s)
        for s1 in s1s:
            s2s = meta.Session.query(Schedule);
            if tid:
                s2s = s2s.filter_by(id=tid)
            s2s = s2s.filter(Schedule.id!=s1.id).all()
            yield "%d to cross against id %d<br />"%(len(s2s),s1.id)
            for s2 in s2s:
                if meta.Session.query(ScheduleIntersectionResult).filter_by(schedule1=s1,schedule2=s2).all():
                    yield '. '
                    continue
                ol = s1.overlaps(s2)
                sir = ScheduleIntersectionResult()
                sir.schedule1 = s1 ; sir.schedule2 = s2
                sir.result=ol
                meta.Session.add(sir)
                meta.Session.commit()
                if ol:
                    yield "<b>overlap</b> between %s (%s-%s , %s days) and %s (%s-%s , %s days) - %s<br />"\
                    %(s1.id
                      ,s1.hours[0].time_from
                      ,s1.hours[0].time_to
                      ,len(s1.weekdays)
                      ,s2.id
                      ,s2.hours[0].time_from
                      ,s2.hours[0].time_to
                      ,len(s2.weekdays)
                      ,ol)
                else: 
                    yield 'no overlap between %s and %s<br />'%(s1.id,s2.id)
            
