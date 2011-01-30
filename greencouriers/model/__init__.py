# -*- coding: utf-8 -*-
"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

#from greencouriers.model import meta
import meta

import datetime

from shapely.geometry import Point,Polygon
from sqlalchemy.orm.interfaces import MapperExtension

from pylons.i18n.translation import _


def now():
	return datetime.datetime.now()

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    ## Reflected tables must be defined and mapped here
    #global reflected_table
    #reflected_table = sa.Table("Reflected", meta.metadata, autoload=True,
    #                           autoload_with=engine)
    #orm.mapper(Reflected, reflected_table)

    sm = orm.sessionmaker(autoflush=True, autocommit=False, bind=engine)

    meta.engine = engine
    meta.Session = orm.scoped_session(sm)

countries_table = sa.Table("countries",meta.metadata,
			   sa.Column("id",sa.types.Integer,primary_key=True)
			   ,sa.Column("name",sa.types.Unicode(),nullable=False,unique=True)
			   ,sa.Column("iso",sa.types.String(),nullable=False,unique=True)
			   ,sa.Column("lon",sa.types.Float())
			   ,sa.Column("lat",sa.types.Float())
			   ,sa.Column("north",sa.types.Float())
			   ,sa.Column("south",sa.types.Float())
			   ,sa.Column("east",sa.types.Float())
			   ,sa.Column("west",sa.types.Float())
,useexisting=True
			   )

class Country(object):
	def __unicode__(self):
		return self.name

orm.mapper(Country,countries_table)


users_table = sa.Table("users",meta.metadata,
                       sa.Column("id",sa.types.Integer,primary_key=True)
			 ,sa.Column("email",sa.types.String(),nullable=True,unique=True)
			 ,sa.Column("password",sa.types.String(),nullable=True)
		       ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
		       ,sa.Column("fb_uid",sa.types.String(),unique=True,nullable=True)
		       ,sa.Column("name",sa.types.Unicode(),unique=False,nullable=True)
		       ,sa.Column("login_hash",sa.types.String(),unique=True)
		       ,sa.Column("lang",sa.types.String(),nullable=False)
		       ,sa.Column("country",sa.types.String(),nullable=False)
		       #,sa.Column("disabled",sa.types.Boolean(),default=False)
		       ,useexisting=True
		       )


class User(object):
	def __unicode__(self):
		return unicode(self.name)
ratings_table = sa.Table("ratings",meta.metadata
			 ,sa.Column("id",sa.types.Integer(),primary_key=True)
			 ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
			 ,sa.Column("by_user_id",sa.ForeignKey("users.id"),nullable=False)
			 ,sa.Column("of_user_id",sa.ForeignKey("users.id"),nullable=False)
			 ,sa.Column("rating",sa.types.Integer(),nullable=False)
			 ,sa.Column("comment",sa.types.Unicode(),nullable=True)
			 ,sa.UniqueConstraint("by_user_id","of_user_id",name='unq_user_rating')
,useexisting=True
)
class Rating(object):
	pass
orm.mapper(User,users_table,properties={
		'ratings_by':orm.relation(Rating,cascade='all, delete, delete-orphan',primaryjoin=ratings_table.c.by_user_id==users_table.c.id)
		,'ratings_of':orm.relation(Rating,cascade='all, delete, delete-orphan',primaryjoin=ratings_table.c.of_user_id==users_table.c.id)
		})

areas_table = sa.Table("areas",meta.metadata,
                       sa.Column("id",sa.types.Integer,primary_key=True)
                       ,sa.Column("user_id",sa.ForeignKey("users.id"),nullable=False)
                       ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
		       ,sa.Column("area_type",sa.types.Unicode(255))
                       ,sa.Column("label",sa.types.Unicode(255),nullable=True)
		       ,sa.Column('area_vol',sa.types.Float())
		       ,sa.CheckConstraint("area_type in ('area','marker')",name='area_type_cstr')
,useexisting=True
)

def intersect_marker_area(a,m):
	point=Point(float(m.points[0].pos_lon),float(m.points[0].pos_lat))

	apoints = [(float(p.pos_lon),float(p.pos_lat)) for p in a.points]
	poly = Polygon(apoints);
	area=poly.area
	if poly.contains(point):
		log.info('poly %s contains point %s'%(poly,point))
		return 100
	else:
		log.info('poly %s does not contain point %s'%(poly,point))
		return False
def intersect_area_area(a1,a2):
	a1points = [(float(p.pos_lon),float(p.pos_lat)) for p in a1.points]
	poly1 = Polygon(a1points);
	area1=poly1.area
	a1.area_vol = area1

	a2points = [(float(p.pos_lon),float(p.pos_lat)) for p in a2.points]
	poly2 = Polygon(a2points);
	area2=poly2.area
	a2.area_vol = area2

	un = poly1.union(poly2)
	joint_area=un.area
	area_diff = abs(area1 + area2 - joint_area)

	if area_diff>0.0001:
		rt= area_diff / area1 * 100
		#raise Exception('here %s , %s'%(area_diff,rt))
                return rt
	else:
		return False

def intersect_marker_marker(m1,m2):
	return False

def compute_area_intersections(a1,against=None):
	if not against:	against = meta.Session.query(Area).filter(Area.id!=a1.id).all() 
	for a2 in against:
		try:
			if a2.area_type=='area':
				if a1.area_type=='marker':
					rt2=rt=intersect_marker_area(a=a2,m=a1)
				elif a1.area_type=='area':
					rt=intersect_area_area(a1=a1,a2=a2)
					rt2=intersect_area_area(a1=a2,a2=a1)
			elif a2.area_type=='marker':
				if a1.area_type=='marker':
					rt2=rt=intersect_marker_marker(m1=a1,m2=a2)
				elif a1.area_type=='area':
					rt2=rt=intersect_marker_area(a=a1,m=a2)
			else: raise Exception('unknown area type, %s'%a2.area_type)
		except ValueError:
			raise Exception('problem crossing against %s'%a2.id)

		if (rt):
			isr=IntersectionResult()
			isr.area1 = a1
			isr.area2 = a2
			isr.result = rt
			meta.Session.add(isr)
		if (rt2):
			isr2=IntersectionResult()
			isr2.area1 = a2
			isr2.area2 = a1
			isr2.result = rt2
			meta.Session.add(isr2)

class AreaMapperExtension(MapperExtension):
	def before_insert(self,mapper,connection,a1):
		compute_area_intersections(a1)

	
class Area(object):
    def __unicode__(self):
        if type(self.label)!=type(None) and len(self.label):
            return self.label
        else:
            if self.area_type=='area':
		    p = Polygon([(p.pos_lon,p.pos_lat) for p in self.points]).centroid
		    rt= _(u'תיחום מ-%s')%(self.entry_stamp.date())
		    cl = getclosestcity(p.x,p.y)
		    if cl: rt+=_(u' באיזור %s')%(cl)
		    return rt
	    elif self.area_type=='marker':
		    p = Point(self.points[0].pos_lon,self.points[0].pos_lat)
		    rt= _(u'מיקום מ-%s')%self.entry_stamp.date()
		    cl =getclosestcity(p.x,p.y)
		    if cl:rt+=_(u' באיזור %s')%(cl)
		    return rt

	    else: raise Exception('unknown area type %s'%self.area_type)

orm.mapper(Area,areas_table,properties={'user':orm.relation(User,backref=orm.backref('areas',cascade='all, delete, delete-orphan'))},extension=AreaMapperExtension())

areas_points_table = sa.Table("areas_points",meta.metadata,
                              sa.Column("id",sa.types.Integer,primary_key=True)
                              ,sa.Column("area_id",sa.ForeignKey("areas.id"))
                              ,sa.Column("pos_lon",sa.types.Float(),nullable=False)
                              ,sa.Column("pos_lat",sa.types.Float(),nullable=False)
,useexisting=True
)
class AreaPoint(object):
	def __unicode__(self):
		return _(u'point %s')%self.id

orm.mapper(AreaPoint,areas_points_table,properties={'area':orm.relation(Area,backref='points',cascade="all, delete, delete-orphan")})

match_notifications_table = sa.Table("match_notifications",meta.metadata
				     ,sa.Column("id",sa.types.Integer(),primary_key=True)
				     ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
				     ,sa.Column("whom_id",sa.ForeignKey('activities.id'),nullable=False)
				     ,sa.Column("of_id",sa.ForeignKey("activities.id"),nullable=False)
				     ,sa.Column("status",sa.types.String(),default='')
				     ,sa.UniqueConstraint("whom_id","of_id",name='unq_whom_of'),useexisting=True)


activities_table = sa.Table("activities",meta.metadata,
			    sa.Column("id",sa.types.Integer,primary_key=True)
			    ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
			    ,sa.Column("user_id",sa.ForeignKey("users.id"),nullable=False)

			    ,sa.Column("area_id",sa.ForeignKey("areas.id"),nullable=True)
			    ,sa.Column("marker_id",sa.ForeignKey("areas.id"),nullable=True)
			    ,sa.CheckConstraint("(area_id is not null or activity_type<>'courier') or (marker_id is not null or activity_type<>'business')",'marker_or_area_constr')

			    ,sa.Column("activity_type",sa.types.Unicode(50),nullable=False)
			    ,sa.Column("business_name",sa.types.Unicode(),nullable=True)
			    ,sa.Column("description",sa.types.Unicode(),nullable=True)
			    ,sa.Column("phone",sa.types.Unicode(15),nullable=True)
			    ,sa.Column("email",sa.types.String(),nullable=True)
			    ,sa.Column("url",sa.types.String(),nullable=True)
			    ,sa.Column("max_delivery_time",sa.types.Integer(),nullable=True)
			    ,sa.Column("deliveries_freq",sa.types.String(),nullable=True)
			    ,sa.CheckConstraint("deliveries_freq in ('rare','occasional','frequent')",name='deliveries_freq_cstr')
			    ,sa.Column("delivery_price",sa.types.Float(),nullable=True)
			    ,sa.Column("address",sa.types.Unicode(100),nullable=True)
			    ,sa.CheckConstraint("activity_type in ('courier','business','client')",name='activity_type_cstr'),useexisting=True)


	
class Activity(object):
	activity_types={'business':u'עסק','courier':u'שליח','client':u'לקוח'}
	def __unicode__(self):
		if self.marker:
			rt = getclosestcity(self.marker.points[0].pos_lon,self.marker.points[0].pos_lat)

		else:
			pt = Polygon([(p.pos_lon,p.pos_lat) for p in self.area.points]).centroid
			rt = getclosestcity(pt.x,pt.y)			
		
		if self.activity_type=='business':
			fa=u'%s , %s'%(self.business_name,_(type(self).activity_types[self.activity_type]))
		else:
			fa='%s, %s'%(self.user.name,_(type(self).activity_types[self.activity_type]))
		return _(u'%s באיזור %s')%(fa,rt)
	pass
class MatchNotification(object):
	pass


orm.mapper(Activity,activities_table,order_by=sa.desc(activities_table.c.id),properties=
	   {
		'user':orm.relation(User,backref=orm.backref('activities',cascade='all, delete, delete-orphan')),
		'area':orm.relation(Area,backref='activities',primaryjoin=activities_table.c.area_id==areas_table.c.id),
		'marker':orm.relation(Area,backref='marked_activities',primaryjoin=activities_table.c.marker_id==areas_table.c.id)
		,'notifications_whom':orm.relation(MatchNotification,primaryjoin=match_notifications_table.c.whom_id==activities_table.c.id,cascade='all, delete, delete-orphan')
		,'notifications_of':orm.relation(MatchNotification,primaryjoin=match_notifications_table.c.of_id==activities_table.c.id,cascade='all, delete, delete-orphan')
		,'ratings':orm.relation(Rating,primaryjoin=activities_table.c.user_id==ratings_table.c.of_user_id,foreign_keys=activities_table.c.user_id,uselist=True)

											 
											 })

schedules_hours_table = sa.Table("schedule_hours",meta.metadata,
				  sa.Column("id",sa.types.Integer,primary_key=True)
				  ,sa.Column("schedule_id",sa.ForeignKey("schedules.id"),nullable=False)
				  ,sa.Column("time_from",sa.types.Time(),nullable=False)
				 ,sa.Column("time_to",sa.types.Time(),nullable=False)
				 ,sa.CheckConstraint("time_to>time_from",'time_range_cstr'),useexisting=True)

schedules_weekdays_table = sa.Table("schedule_weekdays",meta.metadata,
				  sa.Column("id",sa.types.Integer,primary_key=True)
				  ,sa.Column("schedule_id",sa.ForeignKey("schedules.id"),nullable=False)
				  ,sa.Column("weekday",sa.types.Integer(),nullable=False)
				  ,sa.CheckConstraint("weekday>=1 and weekday<=7",name='weekday_boundires'),useexisting=True)



class ScheduleMapperExtension(MapperExtension):
	def after_insert(self,mapper,connection,i):
		#going to compute intersections with all other schedules.
		s2s = meta.Session.query(Schedule).filter(Schedule.id!=i.id).all()
		com=False
		for s2 in s2s:
			over1 = i.overlaps(s2)
			over2 = s2.overlaps(i)
			if over1:
				sir = ScheduleIntersectionResult()
				sir.schedule1 = i ; sir.schedule2 = s2
				sir.result=over1
				meta.Session.add(sir)
				com=True
				#raise Exception('adding schedule1 %s and schedule2 %s'%(i.id,s2.id))
			#if s2.id>14:raise Exception('computing intersection with %d; result: %s'%(s2.id,sir.result))
			if over2:
				sir2 = ScheduleIntersectionResult()
				sir2.schedule1 = s2 ; sir2.schedule2 = i
				sir2.result=over2
				meta.Session.add(sir2)
				com=True
		#if com: meta.Session.commit()
		#raise Exception('just been inseretd %s - %d hour instance(s), %d weekday instance(s)'%(i.id,len(i.hours),len(i.weekdays)))
import logging
log = logging.getLogger(__name__)

schedules_table = sa.Table("schedules",meta.metadata,
			  sa.Column("id",sa.types.Integer,primary_key=True)
			  ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
			   ,sa.Column("activity_id",sa.ForeignKey("activities.id"),nullable=False),useexisting=True)
class Schedule(object):
	def isnow(self):
		n = now()
		myweekdays = [int(md.weekday) for md in self.weekdays]
		wd = int(n.isoweekday()+1)
		if wd==8: wd=1
		if wd not in myweekdays: return False
		if n.time()>=self.hours[0].time_from\
			    and n.time()<=self.hours[0].time_to:
			return True
		return False
	def overlaps(self,o2):
		#first determine if days overlap
		mdays = [int(md.weekday) for md in self.weekdays]
		odays = [int(md.weekday) for md in o2.weekdays]
		rdays = filter(lambda i: i in mdays,odays)
		#raise Exception('%s %s %s'%(mdays,odays,rdays))
		if not len(rdays): return False

		if self.hours[0].time_to<=o2.hours[0].time_from: # i finish before
			log.info('i finish before')
			return False
		elif self.hours[0].time_from>=o2.hours[0].time_to: # i start after
			log.info('i start after') 
			return False
		#i start early
		elif self.hours[0].time_from<=o2.hours[0].time_from and\
			    self.hours[0].time_to<=o2.hours[0].time_to:
			log.info('i start early')
			fr = o2.hours[0].time_from
			to = self.hours[0].time_to
		#i start late
		elif self.hours[0].time_from>=o2.hours[0].time_from and\
			    self.hours[0].time_to>=o2.hours[0].time_to:
			log.info('i start late')
			fr = self.hours[0].time_from
			to = o2.hours[0].time_to
		#i am bigger
		elif self.hours[0].time_from<=o2.hours[0].time_from and\
			    self.hours[0].time_to>=o2.hours[0].time_to:
			log.info('i am bigger')
			fr = o2.hours[0].time_from
			to = o2.hours[0].time_to
		#he is bigger
		elif self.hours[0].time_from>=o2.hours[0].time_from and\
			    self.hours[0].time_to<=o2.hours[0].time_to:
			log.info('he is bigger (%s - %s)'%(o2.hours[0].time_from,o2.hours[0].time_to))
			fr = self.hours[0].time_from
			to = self.hours[0].time_to
		#we're on the same time
		elif self.hours[0].time_from==o2.hours[0].time_from and\
			    self.hours[0].time_to==o2.hours[0].time_to:
			log.info('same time')
			fr = self.hours[0].time_from
			to = self.hours[0].time_to
		else: raise Exception("cannot find intersection state between h %s and h %s"%(self.hours[0].id,o2.hours[0].id)) # between %s - %s and %s - %s"%(self.hours[0].time_form,self.hours[0].time_to,o2.hours[0].time_form,o2.hours[0].time_to))
		from datetime import timedelta
		#raise Exception('(%s-%s) and (%s-%s) : from %s to %s'%(self.hours[0].time_from,self.hours[0].time_to,o2.hours[0].time_from,o2.hours[0].time_to,fr,to))
		timediff = timedelta(hours=to.hour-fr.hour,minutes=to.minute-fr.minute)
		timedifft=timediff*len(rdays)
		#raise Exception('diff time is %s'%timedifft)
		hours=self.hours[0].time_to.hour-self.hours[0].time_from.hour
		minutes = self.hours[0].time_to.minute-self.hours[0].time_from.minute
		#raise Exception('%s hours, %s minutes (%s - %s)'%(hours,minutes,self.hours[0].time_to.minute,self.hours[0].time_from.minute))
		mytm = timedelta(hours=hours,minutes=minutes)
		mytmt=mytm*len(mdays)
		#raise Exception('my time (%s - %s) is %s'%(self.hours[0].time_from.minute,self.hours[0].time_to.minute,mytmt))
		percentage = float(timedifft.days*86400+timedifft.seconds) / float(mytmt.days*86400 + mytmt.seconds)*100
		#raise Exception("(%s-%s,%s) timedifft: %s ; mytmt: %s ; percentage: %s"%(fr,to,len(rdays),timedifft,mytmt,percentage))

		#raise Exception('timediff %s out of %s (%s-%s)'%(timediff,mytm,self.hours[0].time_to,self.hours[0].time_from))
		#raise Exception('%s'%timedifft.seconds)
		return percentage
		#raise Exception('timedifft %s out of %s , percent %s'%(timedifft,mytmt,percentage))
		
		
orm.mapper(Schedule,schedules_table
	   ,extension=ScheduleMapperExtension()
	   ,properties={'activity':orm.relation(Activity,backref=orm.backref('schedules',cascade="all, delete, delete-orphan"))})

class ScheduleHour(object):
	pass
orm.mapper(ScheduleHour,schedules_hours_table,properties={'schedule':orm.relation(Schedule,backref=orm.backref('hours',cascade="all, delete, delete-orphan"))})


class ScheduleWeekday(object):
	pass
orm.mapper(ScheduleWeekday,schedules_weekdays_table,order_by=schedules_weekdays_table.c.weekday,properties={'schedule':orm.relation(Schedule,backref=orm.backref('weekdays',cascade="all, delete, delete-orphan"))})

intersection_results_table = sa.Table("intersection_results",meta.metadata,
			       sa.Column("id",sa.types.Integer,primary_key=True)
			       ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
			       ,sa.Column("area1_id",sa.ForeignKey("areas.id"),nullable=False)
			       ,sa.Column("area2_id",sa.ForeignKey("areas.id"),nullable=False)
			       ,sa.Column("result",sa.types.String(32),nullable=False)
			       ,sa.CheckConstraint("area1_id!=area2_id",name='areas_different')
			       ,sa.UniqueConstraint('area1_id','area2_id',name='unq_areas'),useexisting=True)

class IntersectionResult(object):
	pass

orm.mapper(IntersectionResult,intersection_results_table,properties={
	'area1':orm.relation(Area,primaryjoin=intersection_results_table.c.area1_id==areas_table.c.id,backref=orm.backref('iresults1',cascade='all, delete, delete-orphan')) #,backref=orm.backref('iresults1':cascade='all, delete, delete-orphan'))
		,'area2':orm.relation(Area,primaryjoin=intersection_results_table.c.area2_id==areas_table.c.id,backref=orm.backref('iresults2',cascade='all, delete, delete-orphan')) #)
		});

schedule_overlaps_table = sa.Table("schedule_intersections",meta.metadata,
				   sa.Column("id",sa.types.Integer,primary_key=True)
				   ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
				   ,sa.Column("schedule1_id",sa.ForeignKey("schedules.id"),nullable=False)
				   ,sa.Column("schedule2_id",sa.ForeignKey("schedules.id"),nullable=False)
				   ,sa.UniqueConstraint("schedule1_id","schedule2_id",name="unq_schedules")
				   ,sa.CheckConstraint("schedule1_id != schedule2_id",name='diff_scheds')
				   ,sa.Column("result",sa.types.String(32),nullable=False),useexisting=True)
class ScheduleIntersectionResult(object):
	pass
orm.mapper(ScheduleIntersectionResult,schedule_overlaps_table,properties={
		'schedule1':orm.relation(Schedule,primaryjoin=schedule_overlaps_table.c.schedule1_id==schedules_table.c.id,backref=orm.backref('intersections1',cascade="all, delete, delete-orphan"))
		,'schedule2':orm.relation(Schedule,primaryjoin=schedule_overlaps_table.c.schedule2_id==schedules_table.c.id,backref=orm.backref('intersections2',cascade="all, delete, delete-orphan"))
		})
cities_table = sa.Table("cities",meta.metadata,
			sa.Column("id",sa.types.Integer,primary_key=True)
			,sa.Column("name",sa.types.Unicode(255),unique=False,nullable=False)
			,sa.Column("country",sa.types.String(2),unique=False,nullable=False)
			,sa.UniqueConstraint("name","country",name='unq_name_country')
			,sa.Column("population",sa.types.Integer(),nullable=False)
			,sa.Column("lon",sa.types.Float())
			,sa.Column("lat",sa.types.Float())
			,sa.Column("extent_top",sa.types.Float())
			,sa.Column("extent_left",sa.types.Float())
			,sa.Column("extent_right",sa.types.Float())
			,sa.Column("extent_bottom",sa.types.Float())
,useexisting=True)

class City(object):
	def __unicode__(self):
		return self.name


streets_table = sa.Table("streets",meta.metadata,
			 sa.Column("id",sa.types.Integer,primary_key=True)
			 ,sa.Column("city_id",sa.ForeignKey("cities.id"),nullable=False)
			 ,sa.Column("country",sa.types.String(),unique=False,nullable=False)
			 ,sa.Column("name",sa.types.Unicode(255),unique=False,nullable=False)
			 ,sa.Column("lon",sa.types.Float())
			 ,sa.Column("lat",sa.types.Float())
			 ,sa.Column("extent_top",sa.types.Float())
			 ,sa.Column("extent_left",sa.types.Float())
			 ,sa.Column("extent_right",sa.types.Float())
			 ,sa.Column("extent_bottom",sa.types.Float())
			 ,sa.UniqueConstraint('city_id','name','country',name='unq_city_street_country'),useexisting=True)

#backref=orm.backref('streets',cascade="all, delete, delete-orphan")
class Street(object):
	def __unicode__(self):
		return self.name
orm.mapper(Street,streets_table,properties={
		#'city':orm.relation(City,uselist=False)
		})
orm.mapper(City,cities_table,properties={'streets':orm.relation(Street
								,cascade='all, delete, delete-orphan',backref='city'
								)})

wallposts_table = sa.Table("wallposts",meta.metadata,
			   sa.Column("id",sa.types.Integer,primary_key=True)
			   ,sa.Column("entry_stamp",sa.types.DateTime(),default=now)
			   ,sa.Column("wallpost_type",sa.types.String(),nullable=False)
			   ,sa.Column("activity_id",sa.ForeignKey('activities.id'))
			   ,sa.UniqueConstraint("wallpost_type","activity_id",name="unq_wp_act"),useexisting=True)

class WallPost(object):
	pass

orm.mapper(WallPost,wallposts_table,properties={'activity':orm.relation(Activity,backref='wallposts')})



def getclosestcity(lon,lat):
	qp = Point(lon,lat)
	cities = meta.Session.query(City).filter(cities_table.c.lon!=None).filter(cities_table.c.lat!=None).all()
	if not len(cities): return None
	distances = sorted([(qp.distance(Point(ct.lon,ct.lat)),ct.name) for ct in cities])
	#distances_num = sorted([(qp.distance(Point(ct.lon,ct.lat)),ct.id) for ct in cities]) ; raise Exception('distance from (%s,%s) - %s'%(lon,lat,distances_num))
	rt = distances[0][1]
	return rt


from sqlalchemy import and_,or_,text,literal_column

act = activities_table.alias('act')
a = areas_table.alias('a')
sch = schedules_table.alias('sch')

tact = activities_table.alias('tact')
tsch = schedules_table.alias('tsch')
ta = areas_table.alias('ta')

ir = intersection_results_table.alias('ir')
so = schedule_overlaps_table.alias('so')

res = act.join(sch).join(a,onclause=act.c.area_id==a.c.id)
res2 = tact.join(tsch).join(ta,onclause=tact.c.area_id==ta.c.id)

fres = res.join(ir,onclause=ir.c.area1_id==a.c.id)\
    .join(so,onclause=so.c.schedule1_id==sch.c.id)\
    .join(res2,onclause=and_(ta.c.id==ir.c.area2_id,tsch.c.id==so.c.schedule2_id))
fres = sa.select([act.c.id],from_obj=fres)

business_match_select = sa.select(
	columns=[act.c.id.label('src'),tact.c.id.label('tgt'),ir.c.result.label('ir_res'),so.c.result.label('so_res'),areas_table.c.area_vol.label('area_vol')]
	,from_obj=\
		act.join(sch).join(a,onclause=act.c.marker_id==a.c.id)\
		.join(ir,onclause=ir.c.area1_id==a.c.id)\
		.join(so,onclause=so.c.schedule1_id==sch.c.id)\
		.join(tact,onclause=tact.c.area_id==ir.c.area2_id)\
		.join(tsch,onclause=and_(tsch.c.activity_id==tact.c.id,tsch.c.id==so.c.schedule2_id))\
		.join(areas_table,onclause=tact.c.area_id==areas_table.c.id) #area_vol

	,whereclause=\
		(or_(and_(act.c.activity_type=='courier',tact.c.activity_type=='business')
		     ,and_(act.c.activity_type=='business',tact.c.activity_type=='courier')))
	).order_by(areas_table.c.area_vol.asc()).alias('bms')


class BusinessMatch(object):
	pass
orm.mapper(BusinessMatch,business_match_select
	   ,properties={
		})
		#'source':orm.relation(Activity,viewonly=True,foreign_keys=service_match_select.c.src,primaryjoin=service_match_select.c.src==activities_table.c.id) #,uselist=False,viewonly=True,)


client_match_select = sa.select(
	columns=[act.c.id.label('src')
		 ,tact.c.id.label('tgt')
		 ,ir.c.result.label('ir_res')
		 ,areas_table.c.area_vol.label('area_vol')
		 ]
	,from_obj=\
                act.join(a,onclause=act.c.marker_id==a.c.id)\
                .join(ir,onclause=ir.c.area1_id==a.c.id)\
                .join(tact,onclause=tact.c.area_id==ir.c.area2_id)\
		.join(areas_table,onclause=tact.c.area_id==areas_table.c.id)
	,whereclause=\
                (and_(act.c.activity_type=='client',tact.c.activity_type=='courier'))
	).order_by(areas_table.c.area_vol.asc()).alias('clms')

class ClientMatch(object):
	pass
orm.mapper(ClientMatch,client_match_select
	   ,properties={})

courier_match_select = sa.select(
	columns=[act.c.id.label('src'),tact.c.id.label('tgt'),ir.c.result.label('ir_res'),so.c.result.label('so_res'),areas_table.c.area_vol.label('area_vol')]
	,from_obj=\
		act.join(sch).join(a,onclause=act.c.area_id==a.c.id)\
		.join(ir,onclause=ir.c.area1_id==a.c.id)\
		.join(so,onclause=so.c.schedule1_id==sch.c.id)\
		.join(tact,onclause=tact.c.marker_id==ir.c.area2_id)\
		.join(tsch,onclause=and_(tsch.c.activity_id==tact.c.id,tsch.c.id==so.c.schedule2_id))\
		.join(areas_table,onclause=act.c.area_id==areas_table.c.id) #area_vol
	
	,whereclause=\
		(or_(and_(act.c.activity_type=='courier',tact.c.activity_type=='business'),and_(act.c.activity_type=='business',tact.c.activity_type=='courier')))
	).order_by(sa.sql.expression.cast(ir.c.result,sa.types.Numeric(10,4)).desc()
		   ,sa.sql.expression.cast(so.c.result,sa.types.Numeric(10,4)).desc()).alias('cms')


class CourierMatch(object):
	pass
orm.mapper(CourierMatch,courier_match_select
	   ,properties={
		#'source':orm.relation(Activity,viewonly=True,foreign_keys=service_match_select.c.src,primaryjoin=service_match_select.c.src==activities_table.c.id) #,uselist=False,viewonly=True,)
		})





orm.mapper(MatchNotification,match_notifications_table,properties={
		'whom':orm.relation(Activity,primaryjoin=match_notifications_table.c.whom_id==activities_table.c.id)
		,'of':orm.relation(Activity,primaryjoin=match_notifications_table.c.of_id==activities_table.c.id)
		})


orm.mapper(Rating,ratings_table
	   ,order_by=sa.desc(ratings_table.c.entry_stamp)
	   ,properties={
		'by_user':orm.relation(User,primaryjoin=users_table.c.id==ratings_table.c.by_user_id)
		,'of_user':orm.relation(User,primaryjoin=users_table.c.id==ratings_table.c.of_user_id)
		})

#	   ,allow_null_pks=True
#	   ,primary_key=[act.c.id]

## Non-reflected tables may be defined and mapped at module level
#foo_table = sa.Table("Foo", meta.metadata,
#    sa.Column("id", sa.types.Integer, primary_key=True),
#    sa.Column("bar", sa.types.String(255), nullable=False),
#    )
#
#class Foo(object):
#    pass
#
#orm.mapper(Foo, foo_table)


## Classes for reflected tables may be defined here, but the table and
## mapping itself must be done in the init_model function
#reflected_table = None
#
#class Reflected(object):
#    pass

