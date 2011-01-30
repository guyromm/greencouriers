# -*- coding: utf-8 -*-
import logging

from pylons import request, response, session, tmpl_context as c,url
from pylons.controllers.util import abort, redirect

from greencouriers.lib.base import BaseController, render
from greencouriers.model import meta,User,Activity,Country

log = logging.getLogger(__name__)

from greencouriers.controllers.signup import force_login

import formencode
from pylons.decorators import validate

class UniqueName(formencode.FancyValidator):
    def _to_python(self,value,state):
        us = meta.Session.query(User).filter_by(name=value).filter(User.id!=state.user.id).all()
        if len(us):
            raise formencode.Invalid(u'שם זה כבר בשימוש במערכת',value,state)
        if len(value)>30:
            raise formencode.Invalid(u'אורך מוגבל ל30 תוים',value,state)
        return value

class NameChange(formencode.Schema):
    name = UniqueName(not_empty=True,max_length=30)
    allow_extra_fields=True

class LanguageCountryChange(formencode.Schema):
    lang = formencode.validators.OneOf(['he','en'])
    country = formencode.validators.OneOf([co.iso.lower() for co in meta.Session.query(Country).all()])
    allow_extra_fields=True

class MyAccountController(BaseController):
    @force_login
    def __before__(self):
        from pylons.i18n.translation import _
        c.langs = [('he',_(u'עברית')),('en',_(u'אנגלית'))]
        c.countries = [(co.iso.lower(),'%s (%s)'%(_(co.name),co.name)) for co in meta.Session.query(Country).all()]
        pass
    def fb_login(self):
        return render('/fb_login.html')
    def change_name(self):
        return render('/change_name_form.html')
    def language_country_settings(self):
        c.freemap_url=None; c.use_google_maps=False
        return render('/language_country.html')
    @validate(schema=LanguageCountryChange(),form='language_country_settings',post_only=True,on_get=True,state=c)
    def submit_language_country(self):
        c.user.lang = self.form_result.get('lang')
        c.user.country = self.form_result.get('country')
        meta.Session.commit()
        redirect(url.current(action='index',just_changed=True))
        #raise Exception('submitted %s'%self.form_result)
    @validate(schema=NameChange(),form='change_name',post_only=True,on_get=True,state=c)
    def submit_name_change(self):
        c.user.name = self.form_result.get('name')
        meta.Session.commit()
        redirect(url.current(action='index'))
    def index(self):
        if c.user.country<>'il':
            from greencouriers.controllers.signup import search_country_google
            c.initial_coords=search_country_google(c.user.country)
        from pylons.i18n.translation import get_lang
        #raise Exception('just changed: %s ; user lang: %s ; environ lang: %s'%(request.params.get('just_changed'),c.user.lang,request.environ['pylons.routes_dict']['_lang']))
        if request.GET.get('just_changed')=='True':
            if c.user.lang!=request.environ['pylons.routes_dict']['_lang']:
                #raise Exception('redirecting to lang %s '%c.user.lang)
                redirect(url.current(_lang=c.user.lang))
                return None
        if request.params.get('from_main'):
            acts = meta.Session.query(Activity).filter_by(user_id=c.user.id).all()
            if len(acts)==1:
                return redirect(url.current(controller=acts[0].activity_type,action='matches_map',id=acts[0].id))
        from pylons.i18n.translation import lazify
        c.user_country = meta.Session.query(Country).filter_by(iso=c.user.country.upper()).one()

        c.activities = meta.Session.query(Activity).filter_by(user_id=c.user.id).all()
        return render('/my-account.html')
