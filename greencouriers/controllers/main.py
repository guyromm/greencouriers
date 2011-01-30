# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,Activity,User

log = logging.getLogger(__name__)


from facebook.wsgi import facebook
from greencouriers.controllers.signup import SignupController

from pylons.i18n.translation import _,ungettext,set_lang
import formencode

class SenderValidate(formencode.validators.FancyValidator):
    def _to_python(self,value,state):
        if c.user and c.user.login_hash: return value
        name = formencode.validators.String(not_empty=True)
        name.to_python(value.get('name',''))
        reply_address = formencode.validators.Email(not_empty=True)
        reply_address.to_python(value.get('reply_address',''))
        return value

class ContactForm(formencode.Schema):
    pre_validators=[SenderValidate()]
    subject = formencode.validators.String(not_empty=True)
    message = formencode.validators.String(not_empty=True)
    allow_extra_fields=True
from pylons.decorators import validate
class MainController(SignupController):
#     def __before__(self):
#         c.fb = facebook
#         c.fb.check_session()
#         if c.fb.uid:
#             c.user = meta.Session.query(User).filter_by(fb_uid=c.fb.uid).one()
#             c.user_id = c.user.id
    def samplexc(self):
        raise Exception('sample xception')
    def servejs(self,id):
        import base64,pickle
        st = (base64.b64decode(id)).split(',')
        from pylons import config
        import os,commands
        stdir=(config['pylons.paths']['static_files'])
        rt=''
        for fn in st:
            ffn = os.path.join(stdir,fn[1:])
            ffnm = ffn+'.mini.js'
            if os.path.exists(ffnm) and os.path.getmtime(ffnm)>=os.path.getmtime(ffn):
                pass
                #raise Exception('exists!')
            else:
                cmd = 'java -jar /var/www/pylonsenv/greencouriers/yuicompressor-2.4.2.jar %s -o %s'%(ffn,ffnm)
                sto = commands.getstatusoutput(cmd)
                if (sto[0]!=0): raise Exception('could not compile %s'%ffn)
            nfnh = open(ffnm)
            rt+="\n"+nfnh.read()
            nfnh.close()
        return rt
    def index(self):
        c.nomapjs=True
        if request.params.get('exc',False):
            raise Exception('test exception!')
        #raise Exception('%s'%request.environ['pylons.routes_dict'])
        #raise Exception(_('lang'))
        c.animation=False
        c.activities = meta.Session.query(Activity).all()[0:8]
        #set_lang('he')
        #raise Exception(_('Courier signup'))
        
        c.freemap_url=None; c.use_google_maps=False
        return render('/main-intro.html')
    def contact(self):
        return render('/contact.html')
    @validate(schema=ContactForm(),form='contact',post_only=False,on_get=True,state=c)
    def contact_submit(self):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.header import Header
        msg = MIMEMultipart('alternative')
        msg.set_charset('utf-8')
        msg['Subject'] =  Header(self.form_result.get('subject'),'utf-8')
        txtpref=u''
        if c.user and c.user.email and len(c.user.email):
            msg['Reply-to'] = Header(u'%s <%s>'%(c.user.name,c.user.email),'utf-8')
            #raise Exception('fucking here with "%s"'%c.user.email)
            #raise Exception('%s from %s'%(msg['Reply-to'],c.email)) #self.form_result.get('reply_address')))
        elif c.user and c.user.fb_uid:
            txtpref="message from facebook user %s\n\n"%(c.user.fb_uid)
        else:
            msg['Reply-to'] = Header(u'%s <%s>'%(self.form_result.get('name'),self.form_result.get('reply_address')),'utf-8')

        msg['From']=Header(u'no-reply@greenie.co.il','utf-8')
        msg['To']=Header(u'%s <%s>'%('Guy Romm','guyromm@gmail.com'),'utf-8') #em.email
        part1 = MIMEText((u"%s\n%s"%(txtpref,self.form_result.get('message'))).encode('utf-8'), 'plain','utf-8')        
        msg.attach(part1)
        try:
            s = smtplib.SMTP('localhost')
            s.sendmail('no-reply@greenie.co.il', 'guyromm@gmail.com', msg.as_string())
            c.message=_(u'ההודעה נשלחה בהצלחה!')
        except Exception,e:
            c.message=_(u'ארעה שגיאה בשליחת ההודעה אליך. אנא פנה לתמיכה (guyromm@gmail.com) %s'%e)
        finally:
            if 's' in locals(): s.quit()
        return render('/contacted_succesfully.html')
    def about(self):
        return render('/about.html')
    def faq(self):
        return render('/faq.html')
    def arbitrary_map(self):
        acts = request.params.getall('act')
        c.activities = [meta.Session.query(Activity).get(actid) for actid in acts]
        return render('/arbitrary_map.html')
    def couriers_map(self):
        c.activities = meta.Session.query(Activity).filter_by(activity_type='courier').all()
        return render('/couriers_map.html')
    def businesses_map(self):
        c.activities = meta.Session.query(Activity).filter_by(activity_type='business').all()
        return render('/businesses_map.html')
    def map(self):
        c.activities = meta.Session.query(Activity).all()
        return render('/all_map.html')

