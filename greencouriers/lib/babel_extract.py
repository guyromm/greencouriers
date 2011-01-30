
def countries(a1,a2,a3,options):
    #make_app
    #load_environment(
    #engine = engine_from_config(config, 'sqlalchemy.')
    #init_model(engine)
    from sqlalchemy import create_engine
    from sqlalchemy.sql import select 
    engine = create_engine('postgres://greencouriers:greencouriers@localhost/greencouriers', echo=True,encoding='utf-8')
    conn = engine.connect()
    res=  conn.execute('select id,name from countries')
    try:
        rt= [[int(r[0]),None,r[1].decode('utf8'),''] for r in res]
    except UnicodeDecodeError,e:
        raise Exception('foobar %s (%s)'%(e,r[1]))
    for r in rt:
        try:
            unicode(r[2])
        except:
            print 'cannot parse %s'%r[1]
    #raise Exception('got to end')
    conn.close()
    return rt
        #raise Exception('%s'%res['name'])

