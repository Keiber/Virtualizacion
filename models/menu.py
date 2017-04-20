response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = [
(T('Index'),URL('default','index')==URL(),URL('default','index'),[]),
(T('User'),URL('default','user_manage')==URL(),URL('default','user_manage'),[]),
(T('Profesor'),URL('default','profesor')==URL(),URL('default','profesor'),[]),
(T('Disenador'),URL('default','disenador')==URL(),URL('default','disenador'),[]),
(T('Course'),URL('default','course_manage')==URL(),URL('default','course_manage'),[]),
(T('Recurso'),URL('default','recurso')==URL(),URL('default','recurso'),[]),
(T('Program'),URL('default','program_manage')==URL(),URL('default','program_manage'),[]),
(T('Has Course'),URL('default','has_course_manage')==URL(),URL('default','has_course_manage'),[]),
(T('Register User'),URL('default','register_user')==URL(),URL('default','register_user'),[]),
(T('Dashboard'),URL('default','dashboard')==URL(),URL('default','dashboard'),[]),
]