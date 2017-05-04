@auth.requires_login()
def get_courses_data():
    courses = dict(data = db(db.t_course).select(db.t_course.f_code, db.t_course.f_name))
    return courses

@auth.requires_login()
def get_programs_data():
    programs = dict(data = db(db.t_program.f_level == 0).select())
    return programs

@auth.requires_login()
def get_users():
	users = dict(data = db(db.auth_user).select())
	return users



