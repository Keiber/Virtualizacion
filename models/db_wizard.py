### we prepend t_ to tablenames and f_ to fieldnames for disambiguity

########################################
db.define_table('t_program',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_modality', type='string',
          label=T('Modality')),
    Field('f_code', type='string', unique = True,
          label=T('Code')),
    Field('f_date_start', type='date',
          label=T('Date Start')),
    Field('f_date_end', type='date',
          label=T('Date End')),
    Field('f_level', type='integer',
          label=T('Level')),
    Field('f_duration', type='integer',
          label=T('Duration')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

#db.define_table('t_program_archive',db.t_program,Field('current_record','reference t_program',readable=False,writable=False))

########################################### PROYECTO

db.define_table('t_project',
    Field('f_program', type='reference t_program',
          label=T('Program')),
    Field('f_progress', type='string',
          label=T('Progress')),
    auth.signature,
    format='%(f_program)s',
    migrate=settings.migrate)

#db.define_table('t_project_archive', db.t_project,Field('current_record','reference t_project', readable=False, writable=False))


########################################

db.define_table('t_has_program',
    Field('f_program_a', type='reference t_program',
         label=T('Program_a Has')),
    Field('f_program_b', type='reference t_program',
         label=T('Program_b Has')),
     auth.signature,
    format='%(f_program_has)s',
    migrate=settings.migrate)

#db.define_table('t_has_program_archive', db.t_has_program,Field('current_record','reference t_has_program', readable=False, writable=False))


########################################

db.define_table('t_usuario',
    Field('f_first_name', type='string',
          label=T('First Name')),
    Field('f_username', type='string',
          label=T('Username')),
    Field('f_last_name', type='string',
          label=T('Last Name')),
    Field('f_email', type='string', unique = True,
          label=T('Email')),
    Field('f_password', type='string',
          label=T('Password')),
    Field('f_type_user', type='string',
          label=T('Type User')),
    Field('f_notification', type='string',
          label=T('Notification')),
    auth.signature,
    format='Username: %(f_username)s ID: %(id)s',
    migrate=settings.migrate)

#db.define_table('t_usuario_archive',db.t_usuario,Field('current_record','reference t_usuario',readable=False,writable=False))

########################################

db.define_table('t_course',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_modality', type='string',
          label=T('Modality')),
    Field('f_code', type='string', unique = True,
          label=T('Code')),
    Field('f_responsable', type='reference t_usuario',
          label=T('Responsable')),
    Field('f_duration', type='integer',
          label=T('Duration')),
    auth.signature,
    format='Nombre: %(f_name)s ID: %(f_code)s',
    migrate=settings.migrate)

#db.define_table('t_course_archive',db.t_course,Field('current_record','reference t_course',readable=False,writable=False))


########################################

db.define_table('t_has_course',
    Field('f_program_has', type='reference t_program',
          label=T('Program Has')),
    Field('f_course_has', type='reference t_course',
          label=T('Course Has')),
    auth.signature,
    format='%(f_program_has)s',
    migrate=settings.migrate)

#db.define_table('t_has_course_archive',db.t_has_course,Field('current_record','reference t_has_course',readable=False,writable=False))

########################################

db.define_table('t_unity',
    Field('f_course', type='reference t_course',
          label=T('Course')),
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_objective', type='text',
          label=T('Objective')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

#db.define_table('t_unity_archive',db.t_unity,Field('current_record','reference t_unity',readable=False,writable=False))


############################################# TEMA 

db.define_table('t_topic',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_objective', type='text',
          label=T('Objective')),
    Field('f_unity', type='reference t_unity',
          label=T('Unity')),
    Field('f_modality', type='string',
          label=T('Modality')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

#db.define_table('t_topic_archive',db.t_topic,Field('current_record','reference t_topic',readable=False,writable=False))

######################################## Agregado E K
db.define_table('t_resource',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_area', type='string',
          label=T('Area')),
    Field('f_code_topic', type='reference t_topic',
          label=T('CodeCourse')),
    Field('f_responsable', type='reference t_usuario',
          label=T('Responsable')),
    Field('f_type', type='string',
          label=T('Type')),
    Field('f_format', type='string',
          label=T('Format')),
    Field('f_description', type='string',
           label=T('Description')),
    Field('f_is_planilla', type='boolean',
           label=T('is_planilla')),
    Field('f_is_verificado', type='boolean',
           label=T('is_verificado')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

#db.define_table('t_recurso_archive',db.t_resource,Field('current_record','reference t_resource',readable=False,writable=False))

######################################## Agregado E K

db.define_table('t_file',
    Field('f_name', type='string',
          label=T('Name')),
    Field('f_code_resource', type='reference t_resource',
          label=T('CodeResource')),
    Field('f_description', type='string',
           label=T('Description')),
    Field('f_responsable', type='reference t_usuario',
           label=T('Responsable')),
    Field('f_file','upload',
            label=T('File')),
    auth.signature,
    format='%(f_name)s',
    migrate=settings.migrate)

#db.define_table('t_file_archive',db.t_file,Field('current_record','reference t_file',readable=False,writable=False))


############################################ 

db.define_table('t_notification_course',
    Field('f_usuario', type='reference t_usuario',
          label=T('Creator')),
    Field('f_curso', type='reference t_course',
          label=T('Curso al que pertenece')),
    Field('f_title', type='string',
          label=T('Title')),
    Field('f_viewed', type='boolean',
          label=T('Viewed')),
    Field('f_content', type='text',
          label=T('Content')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))


############################################ 

db.define_table('t_notification_resource',
    Field('f_usuario', type='reference t_usuario',
          label=T('Creator')),
    Field('f_resource', type='reference t_resource',
          label=T('Recurso al que pertenece')),
    Field('f_title', type='string',
          label=T('Title')),
    Field('f_viewed', type='boolean',
          label=T('Viewed')),
    Field('f_content', type='text',
          label=T('Content')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))


############################################ 

db.define_table('t_notification_file',
    Field('f_usuario', type='reference t_usuario',
          label=T('Creator')),
    Field('f_file', type='reference t_file',
          label=T('Archivo al que pertenece')),
    Field('f_title', type='string',
          label=T('Title')),
    Field('f_viewed', type='boolean',
          label=T('Viewed')),
    Field('f_content', type='text',
          label=T('Content')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))

############################################ 

db.define_table('t_permisology_course',
    Field('f_usuario', type='reference t_usuario',
          label=T('Usuario')),
    Field('f_curso', type='reference t_course',
          label=T('Curso al que tiene permisologia')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))


############################################ 

db.define_table('t_permisology_resource',
    Field('f_usuario', type='reference t_usuario',
          label=T('Usuario')),
    Field('f_resource', type='reference t_resource',
          label=T('Recurso al que tiene permisologia')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))


############################################ 

db.define_table('t_permisology_file',
    Field('f_usuario', type='reference t_usuario',
          label=T('Usuario')),
    Field('f_file', type='reference t_file',
          label=T('Archivo al que tiene permisologia')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)

#db.define_table('t_notification_archive', db.t_notification,Field('current_record','reference t_notification', readable=False, writable=False))


############################################ 

db.define_table('t_notification',
    Field('f_usuario_a', type='integer',
          label=T('Usuario_a')),
    Field('f_usuario_b', type='integer',
          label=T('Usuario_b')),
    Field('f_tittle', type='string',
          label=T('Tittle')),
    Field('f_viewed', type='boolean',
          label=T('Viewed')),
    Field('f_content', type='text',
          label=T('Content')),
    auth.signature,
    format='%(t_notification)s',
    migrate=settings.migrate)