"""Setup the greencouriers application"""
import logging

from greencouriers.config.environment import load_environment

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup greencouriers here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Load the models
    from greencouriers.model import meta,User
    meta.metadata.bind = meta.engine

    # Create the tables if they aren't there already
    meta.metadata.create_all(checkfirst=True)
    if False and not len(meta.Session.query(User).all()): #cancelled for now
	u = User()
	u.id=1
	meta.Session.add(u)
	meta.Session.commit()
	
