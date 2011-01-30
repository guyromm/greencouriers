import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Activity,IntersectionResult,Area
from sqlalchemy.orm.exc import NoResultFound
from shapely.geometry import Polygon,Point
log = logging.getLogger(__name__)

class IntersectionsController(BaseController):
    def do(self,id):
        from greencouriers.model import compute_area_intersections
        compute_area_intersections(meta.Session.query(Area).get(id),[meta.Session.query(Area).get(request.params.get('against'))])
        return 'computed'
    def compareas(self):
        areas = meta.Session.query(Area).filter_by(area_type='area',area_vol=None).all() ; cnt=0 ; failcnt=0
        for a in areas:
            
            bpoints = [(p.pos_lon,p.pos_lat) for p in a.points]
            try:
                bpoly = Polygon(bpoints)
                area = bpoly.area
                log.info('%s is %s'%(a.id,area))
                a.area_vol = area
                meta.Session.commit()
                cnt+=1
            except Exception,e:
                log.info('area %s threw %s'%(a.id,unicode(e)))
                failcnt+=1
        return 'done %s, failed %s'%(cnt,failcnt)
    def index(self):
        return 'foo'
        rt=''
        businesses = meta.Session.query(Activity).filter_by(activity_type='business').all()
        couriers = meta.Session.query(Activity).filter_by(activity_type='courier').all()
        rt+="scanning %d businesses\n"%len(businesses)
        rt+="and %d couriers\n"%len(couriers)
        for b in businesses:
            if len(b.area.points)<3:
                rt+="skipping business %d because of insufficient points (%d)\n"%(b.id,len(b.area.points))
                continue
            bpoints = [(p.pos_lon,p.pos_lat) for p in b.area.points]
            bpoly = Polygon(bpoints)
            business_area=bpoly.area
            business_marker=Point(b.marker.points[0].pos_lon,b.marker.points[0].pos_lat)
            for bf in ['marker','area']:
                for cr in couriers:
                    if cr.area==b.area:
                        rt+="skipping activities %d and %d for they use the same area\n"%(b.area.id,cr.area.id) 
                        continue
                    #let's see if we have a match.
                    if cr.area.id>getattr(b,bf).id:
                        area1_id = cr.area.id
                        area2_id = getattr(b,bf).id
                    else:
                        area2_id = cr.area.id
                        area1_id = getattr(b,bf).id
                    try:
                        isr=meta.Session.query(IntersectionResult).filter_by(area1_id=area1_id,area2_id=area2_id).one()
                        rt+=". "
                        continue
                    except NoResultFound:
                        isr=IntersectionResult()
                        isr.area1_id=area1_id
                        isr.area2_id=area2_id

                    cpoints = [(p.pos_lon,p.pos_lat) for p in cr.area.points]
                    cpoly = Polygon(cpoints)
                    courier_area=cpoly.area
                    #check if areas overlap or contain each other
                    if bf=='area':
                        try:
                            un = bpoly.union(cpoly)
                        except:
                            rt+="exception between business %d and courier %d\n"%(b.id,cr.id)
                            rt+="courier is %s\n"%cpoly
                        joint_area=un.area
                        area_diff = abs(courier_area + business_area - joint_area)
                        if area_diff>0.0001:
                            isr.result='match'
                            rt+="WE HAVE A MATCH (%f)! business %d (area %d) and courier %d (area %d)\n"%(abs(area_diff),b.id,b.area.id,cr.id,cr.area.id)
                        else:
                            isr.result='mismatch'
                    #check if business location within couriers area
                    elif bf=='marker':
                        if cpoly.contains(business_marker):
                            isr.result='match'
                            rt+='COURIER AREA %s contains business mark %s\n'%(courier_area,business_marker)
                        else:
                            isr.result='mismatch'
                    else:
                        raise Exception('unknown bf %s'%bf)
                    
                    meta.Session.add(isr)
                    if not request.params.get('nocommit'):
                        meta.Session.commit()

        c.output=rt
        return render('/intersections.html')
