# -*- coding: utf-8 -*-
import logging

from pylons import config, request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import User,meta

log = logging.getLogger(__name__)

import formencode
from pylons.decorators import validate

class NoDupeUser(formencode.FancyValidator):
    def _to_python(self,value,state):
        emv = value['email']
        u = meta.Session.query(User).filter_by(email=emv).all()
        if len(u):
            raise formencode.Invalid(None,value,state,error_dict={'email':u'כבר קיים משתמש עם המייל הנ"ל'})
        return value


class AuthUser(formencode.FancyValidator):
    def _to_python(self,value,state):
        try:
            u = meta.Session.query(User).filter_by(email=value['email']).one()
        except:
            raise formencode.Invalid(None,value,state,error_dict={'email':u'לא קיים משתמש עם המייל הנ"ל'})
        if u.password!=value['password']:
            raise formencode.Invalid(None,value,state,error_dict={'password':u'סיסמא שגויה'})
        return value
class ExistingUser(formencode.FancyValidator):
    def _to_python(self,value,state):
        try:
            u = meta.Session.query(User).filter_by(email=value['email']).one()
        except:
            raise formencode.Invalid(None,value,state,error_dict={'email':u'לא קיים משתמש עם המייל הנ"ל'})
        return value
class AccountSignup(formencode.Schema):
    email = formencode.validators.Email(not_empty=True)
    password = formencode.validators.MinLength(6,not_empty=True)
    repeat_password = formencode.validators.String(not_empty=True)    
    return_url=formencode.validators.String()
    chained_validators = [formencode.validators.FieldsMatch('password','repeat_password'),NoDupeUser()]
    allow_extra_fields=True

class AccountLogin(formencode.Schema):
    email = formencode.validators.Email(not_empty=True)
    password = formencode.validators.String(not_empty=True)
    return_url=formencode.validators.String()
    chained_validators = [AuthUser()]

    allow_extra_fields=True
class ResetPassword(formencode.Schema):
    email = formencode.validators.Email(not_empty=True)
    chained_validators = [ExistingUser()]
    allow_extra_fields=True
from greencouriers.controllers.signup import SignupController
import os
def default_user_attrs(u,req):
    #first, get the user's country by ip - 
    import pygeoip
    dn = os.path.join(config['pylons.paths']['root'],'..','GeoIP.dat')
    gi = pygeoip.GeoIP(dn,pygeoip.GEOIP_MEMORY_CACHE)
    country_code = gi.country_code_by_addr(str(request.environ['REMOTE_ADDR']))

    if not country_code: 
        country_code = config['global_conf']['default_country']
    country_code=country_code.lower()
    if country_code=='il': 
        lang='he'
    else:
        lang='en'
    u.lang = lang
    u.country = country_code
    log.info('assigning user attributes - country %s , language %s'%(country_code,lang))
    return None


class AuthController(SignupController):
    activity_type='none'
    @validate(schema=AccountSignup(),form='index',post_only=False,on_get=True,state=c)
    def signup(self):
        u = User()
        for fn in ['email','password','name']:
            setattr(u,fn,self.form_result.get(fn))
        u.fb_uid=None
        default_user_attrs(u,request)
        #override lang with the lang user signed up in
        u.lang = request.environ['pylons.routes_dict']['_lang']
        meta.Session.add(u); meta.Session.commit()
        return self.login()
    @validate(schema=ResetPassword(),form='index',post_only=False,on_get=True,state=c)
    def reset(self):
        u = meta.Session.query(User).filter_by(email=self.form_result.get('email')).one()
        import sha
        import time
        u.password = sha.new(str(time.time())+u.email+config['pw_reset_salt']).hexdigest()[0:6]
        meta.Session.commit()

        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.header import Header
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')
        msg['Subject'] =  Header(u'איפוס סיסמה','utf-8')
        msg['From']=Header(u'no-reply@greenie.co.il','utf-8')
        msg['To']=Header(u'%s <%s>'%(u.name,u.email),'utf-8') #em.email
        part1 = MIMEText((u'סיסמתך החדשה הינה %s'%u.password).encode('utf-8'), 'plain','utf-8')        
        msg.attach(part1)
        try:
            c.message=u'סיסמתך אופסה ונשלחה אליך בדוא"ל.'
            s = smtplib.SMTP('localhost')
            s.sendmail('no-reply@greenie.co.il', u.email, msg.as_string())
        except:
            c.message=u'ארעה שגיאה בשליחת הסיסמה החדשה אליך. אנא פנה לתמיכה (guyromm@gmail.com)'
        finally:
            if 's' in locals(): s.quit()
        return self.index()
    @validate(schema=AccountLogin(),form='index',post_only=False,on_get=True,state=c)
    def login(self):
        u = meta.Session.query(User).filter_by(email=self.form_result.get('email'),password=self.form_result.get('password')).one()
        import sha,time
        u.login_hash = sha.new(str(time.time())+u.email+config['pw_login_salt']).hexdigest()
        meta.Session.commit()
        session['greenie_auth']=u.login_hash; session.save()

        if request.params.get('return_url'):
            return redirect(str(request.params.get('return_url')))
    def logout(self):
        if c.user:
            c.user.login_hash=None
            meta.Session.commit()
        if 'greenie_auth' in session:
            del session['greenie_auth'];session.save();
        
        from facebook.wsgi import facebook
        # looks like fb does not have .logout() :/
        # sess = facebook.check_session()
        # if sess:
        #    facebook.logout()

        return redirect(url.current(controller='main',action='index'))
    def index(self):
        return self.fb_login()
    
