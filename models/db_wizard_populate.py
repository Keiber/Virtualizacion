from gluon.contrib.populate import populate
if db(db.auth_user).isempty():
     populate(db.auth_user,10)
     populate(db.t_program,10)
     populate(db.t_course,10)
     populate(db.t_has_course,10)
     populate(db.t_usuario,10)
