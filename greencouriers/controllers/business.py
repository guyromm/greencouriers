# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Activity,BusinessMatch,MatchNotification,WallPost,User,Rating

from sqlalchemy.orm.exc import NoResultFound


from facebook.wsgi import facebook
import formencode

log = logging.getLogger(__name__)
from pylons.decorators import validate
from pylons.i18n.translation import _

def load_user():
    sess = facebook.check_session()
    from pylons import config
    if sess:
        c.user = meta.Session.query(User).filter_by(fb_uid=facebook.uid).one()
    elif config['use_facebook']!='true':
        c.user = meta.Session.query(User).get(1)        


from greencouriers.controllers.signup import weekdays


class PreventDupes(formencode.validators.FancyValidator):
    def _to_python(self,val,state):
        load_user()
        activity_id = request.environ['pylons.routes_dict']['id']
        act = meta.Session.query(Activity).get(activity_id)
        #raise Exception('by user %s, of user %s'%(state.user.id,act.user_id))
        qres = meta.Session.query(Rating).filter_by(by_user=state.user
                                                    ,of_user_id=act.user_id).all()
        if qres:
            raise formencode.Invalid(None,val,state,error_dict={'general':_(u'כבר נתת ציון לשירות זה.')})
        return val
class Critique(formencode.Schema):
    pre_validators = [PreventDupes()]
    rating = formencode.validators.Number(not_empty=True)
    comment = formencode.validators.MaxLength(maxLength=100,not_empty=False)
    allow_extra_fields=True

def load_matches(id,match_type):
    mqry = meta.Session.query(match_type).filter_by(src=id)
    service_matches = mqry.all()
    for cm in service_matches:
        cm.activity = meta.Session.query(Activity).get(cm.tgt)
    return service_matches
    
class BusinessController(BaseController):
    show_sched=True
    activity_type='business'
    match_type=BusinessMatch
    def __before__(self):
        c.show_sched = type(self).show_sched
    def wallpost_done(self,id):
        a = meta.Session.query(Activity).get(id)
        wp = meta.Session.query(WallPost).filter_by(wallpost_type='service_creation',activity=a).all()
        if not wp:
            wp = WallPost()
            wp.activity = a
            wp.wallpost_type='service_creation'
            meta.Session.add(wp) ; meta.Session.commit()
        return 'jukcess'
    def load_matches(self,id):
        c.service_matches = load_matches(id,type(self).match_type)
        c.maxvol=0
        c.minvol=100
        for cm in c.service_matches:
            if hasattr(cm,'area_vol'):
                if cm.area_vol<c.minvol:  c.minvol=cm.area_vol
                if cm.area_vol>c.maxvol: c.maxvol=cm.area_vol
        #raise Exception('%s - %s'%(c.minvol,c.maxvol))
    matches_heading=_(u'רשימת עסקים הזקוקים לשליח באיזור שלך')
    def matches_map(self,id):
        c.weekdays = weekdays
        self.load_matches(id)

        if request.params.get('justadded') and not len(c.service_matches):
            return redirect(url.current(action='index',id=id,justadded=True))
        act = meta.Session.query(Activity).get(id)
        if not act: abort(404)
        c.act = act
        c.activities = [cm.activity for cm in c.service_matches]
        c.title=_(u'התאמות שירות ל%s')%act
        self.justadded(c.act)
        if request.params.get('print',False):
            return render('/%s_matches_map_print.html'%act.activity_type)
        else:
            return render('/%s_matches_map.html'%act.activity_type)
    def index(self,id):
        if id=='TOKEN': abort(404)
        c.b = meta.Session.query(Activity).get(id)
        if not c.b:
            abort(404)
        if c.b.activity_type!=type(self).activity_type: raise Exception('is not a business!')
        c.weekdays = weekdays
        self.load_matches(id)
        #now, make sure we notified everyone about the matches :D
        self.justadded(c.b);    
        load_user()

        if c.user and self._can_comment(c.user.id,c.service_matches):
            c.can_comment=True
        return render('/business.html')
    def justadded(self,act):
        
        acts_text = {'business':_(u'עסק'),'courier':_(u'שליח'),'client':_(u'לקוח')}

        sess = facebook.check_session()

        to_notify=[]; to_notify_email=[]
        for cm in c.service_matches:
            #if not sess: continue
            notif = meta.Session.query(MatchNotification).filter_by(of=act,whom=cm.activity).all()
            if not notif:
                notif = MatchNotification()
                notif.whom = cm.activity
                #cm.activity.notifications_whom.append(notif)
                if notif.whom.user.fb_uid not in to_notify: to_notify.append(notif.whom.user.fb_uid)
                if notif.whom.user.email!=None and len(notif.whom.user.email)>0 and notif.whom.user.email not in to_notify_email:
                    to_notify_email.append(notif.whom.user.id)
                notif.of = act
                act.notifications_of.append(notif)
                meta.Session.add(notif); 
                meta.Session.commit()
                log.info('notifying %s of %s'%(notif.whom,notif.of))
            else:
                notif = notif[0]
        if sess and len(to_notify):
            from facebook import FacebookError
            try:
                facebook.notifications.send(to_notify
                                            ,_(u'רשם שירות באתר <a href="http://www.greenie.co.il/">השליחים הירוקים</a> וישנה התאמה ביניכם - <a href="http://www.greenie.co.il%s">%s</a>')
                                            %(url.current(controller=act.activity_type,action='index',id=act.id),act))
                notif.status+='facebook-success;'
            except FacebookError:
                log.error('could not send notifications to %s in session %s'%(to_notify,sess))
                notif.status+='facebook-failed;'
                meta.Session.commit()
                return None
        #email notification - 
        #raise Exception(to_notify_email)
        for tuid in to_notify_email:
            u = meta.Session.query(User).get(tuid)
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.header import Header
            #this is quite the stupid HACK:
            if type(notif.of)==Activity:
                act = notif.of
            else:
                act = notif.of[0]

            msg = MIMEMultipart('alternative')
            msg.set_charset('utf-8')
            msg['Subject'] =  Header(_(u'התאמה חדשה בגריני'),'utf-8')
            msg['From']=Header(u'no-reply@greenie.co.il','utf-8')
            msg['To']=Header(u'%s <%s>'%(u.name,u.email),'utf-8') #em.email
            html = (_(u'התאמה חדשה בגריני - <a href="%s">לצפיה</a>')%url.current(controller=act.activity_type,action='index',id=act.id,qualified=True))
            part1 = MIMEText(html.encode('utf-8'), 'html','utf-8')        
            msg.attach(part1)
            try:
                s = smtplib.SMTP('localhost')
                s.sendmail('no-reply@greenie.co.il', u.email, msg.as_string())
                notif.status+='email-success;'
            except:
                notif.status+='email-failed;'
                meta.Session.commit()
            finally:
                if 's' in locals(): s.quit()
        #wallpost!
        if sess and request.params.get('justadded') and not meta.Session.query(WallPost).filter_by(wallpost_type='service_creation',activity=act).all():
            c.wall_entry_act=act 
            c.wall_entry_dialog=True
            c.wall_entry_params={'url':'http://www.greenie.co.il%s'%(url.current(controller=act.activity_type,action='index',id=act.id)),'signup_type':acts_text[act.activity_type],'actor':act.user.name}
            
    @validate(schema=Critique(),form='index',post_only=False,on_get=True,state=c)
    def critique(self,id):
        load_user()
        self.load_matches(id)
        act = meta.Session.query(Activity).get(id)
        if c.user and self._can_comment(c.user.id,c.service_matches):
            rt = Rating()
            #raise Exception('inserting rating by user %s of user %s'%(c.user.id,act.user.id))
            rt.by_user = c.user
            #rt.by_user_id = c.user.id
            #c.user.ratings_by.append(rt)
            rt.of_user = act.user
            #rt.of_user_id = act.user.id
            act.user.ratings_of.append(rt)
            rt.rating = self.form_result.get('rating')
            rt.comment = self.form_result.get('comment')
            meta.Session.add(rt)
            meta.Session.commit()
            sess = facebook.check_session()
            if sess:
                facebook.notifications.send([act.user.fb_uid]
                                            ,_(u' נתן ציון לשירותך באתר <a href="http://www.greenie.co.il/">השליחים הירוקים</a> - <a href="http://www.greenie.co.il%s">%s</a>')%(url.current(controller=act.activity_type,action='index',id=act.id),act))
            redirect(url.current(action='index',id=id))
        else: raise Exception('permission denied to comment for this user here')

    def _can_comment(self,user_id,service_matches):
        if user_id in [act.activity.user_id for act in service_matches]:
            return True
        else:
            return False

