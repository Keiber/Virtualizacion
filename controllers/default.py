# -*- coding: utf-8 -*-
### required - do no delete
# Some imports
from time import gmtime, strftime
import json

def user(): return dict(form=auth())
def download(): return response.download(request,db)
def call(): return service()
### end requires
@auth.requires_login()
def index():
    # id = auth.id  -> res = db(db.t_usuario.id == id ).select() -> res.f_type
    #if es instruccional renderizar vista de instruccional ...
    #return 

    res = db(db.t_program).select()
    n = 0
    res_n = 0
    for row in res:
        res_n=res_n+1
    notificacion = db(db.t_notification.f_usuario_b == auth.user.id).select()
    usuarios = []
    for row in notificacion:
        usuarios.append( db(db.t_usuario.id == row.f_usuario_a).select(db.t_usuario.f_first_name, distinct=False) )
        n=n+1

    usuarios_sistema = db(db.t_usuario).select()

    return dict(query=res, length_query = res_n, notification = notificacion, length_notification = n, notification_emited = usuarios, users = usuarios_sistema, length_users = len(usuarios_sistema))

def error():
    return dict()


@auth.requires_login()
def create_notif():
    user_emisor, user_receptor, titulo, contenido = auth.user.id, request.post_vars['user_receptor'], request.post_vars['titulo'], request.post_vars['contenido']
    select = db(db.t_usuario.f_first_name == user_receptor).select()
    id_receptor = 0
    for row in select:
        id_receptor = row.id
    db.t_notification.insert(
        f_usuario_a = user_emisor,
        f_usuario_b = id_receptor,
        f_tittle = titulo,
        f_viewed = False,
        f_content = contenido
        )    
    return index()

@auth.requires_login()
def insert():
    user_name, name, last_name, user_type, email, password = request.post_vars['user_name'],request.post_vars['name'], request.post_vars['last_name'], request.post_vars['user_type'], request.post_vars['email'], request.post_vars['password']
    db.t_usuario.insert(
            f_username=user_name,
            f_first_name=name,
            f_last_name=last_name,           
            f_email=email,
            f_password=db.auth_user.password.requires[0](password)[0],
            f_type_user=user_type,
            f_notification="0"
        )
    db.auth_user.insert(
            first_name=name,
            last_name=last_name,           
            email=email,
            password=db.auth_user.password.requires[0](password)[0],           
        )
    return dict() 

@auth.requires_login()
def registrar_usuario():
    return dict()

@auth.requires_login()
def user_manage():
    return dict()

@auth.requires_login()
def course_manage():
    form = SQLFORM.smartgrid(db.t_course,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def has_course_manage():
    form = SQLFORM.smartgrid(db.t_has_course,onupdate=auth.archive)
    return locals()

@auth.requires_login()
def register_user():
    return dict()

@auth.requires_login()
def dashboard():
    return dict()

@auth.requires_login()
def validar_form_recurso(form):
    c = form.vars.f_name
    t = form.vars.f_type
    f = form.vars.f_format
    d = form.vars.f_description
    c = c.strip()
    t = t.strip()
    f = f.strip()
    d = d.strip()
    if c=="" or t=="" or f=="" or d=="":
        form.errors.f_name = 'todos los campos deben estar llenos'
        form.errors.f_type = 'todos los campos deben estar llenos'
        form.errors.f_format = 'todos los campos deben estar llenos'
        form.errors.f_description = 'todos los campos deben estar llenos'

@auth.requires_login()
def validar_form_archivo(form):
    c = form.vars.f_name
    d = form.vars.f_description
    a = form.vars.f_file
    c = c.strip()
    d = d.strip()
    a = a.strip()
    if c=="" or d=="" or a=="":
        form.errors.f_name = 'todos los campos deben estar llenos'
        form.errors.f_description = 'todos los campos deben estar llenos'
        #form.vars.f_file = 'todos los campos deben estar llenos'

@auth.requires_login()
def recurso():
    #form =db().select(db.t_resource.f_name, db.t_resource.f_code_course)
    form = SQLFORM(
        db.t_resource,
        fields=['f_name','f_code_course','f_responsable','f_type','f_format','f_description','f_is_planilla'],
        deletable=True)
    if form.process(onvalidation=validar_form_recurso).accepted:
        response.flash = 'Recurso aceptado'
    elif form.errors:
        response.flash = 'Error de formulario'
    return dict(form=form)

@auth.requires_login()
def display_planillas():
    form = SQLFORM.smartgrid(db.t_resource, constraints = dict(t_resource = db.t_resource.f_is_planilla == True),
        onupdate=auth.archive,
        deletable=False,
        editable=False,
        searchable=False,
        create=False,
        csv=False,
        showbuttontext=False)
    return locals()



@auth.requires_login()
def display_resources():
    query = db.t_resource.f_is_planilla == False
    form = SQLFORM.smartgrid(
        db.t_resource,
        constraints = dict(t_resource = query),
        onupdate=auth.archive,
        deletable=False,
        editable=False,
        searchable=False,
        create=False,
        csv=False,
        showbuttontext=False
        )
    return locals()


@auth.requires_login()
def verificar_planillas():
    id_resource = request.post_vars['id_resource']
    row = db(db.t_resource.id == id_resource).select().first()
    row.update_record(f_is_verificado=True)
    redirect(URL('display_planillas'))  
    #return locals()

@auth.requires_login()
def verificar_resources():
    id_resource = request.post_vars['id_resource']
    row = db(db.t_resource.id == id_resource).select().first()
    row.update_record(f_is_verificado=True)
    redirect(URL('display_resources'))  
    #return locals()

@auth.requires_login()
def desverificar_resources():
    id_resource = request.post_vars['id_resource']
    comentario = request.post_vars['comment']
    row = db(db.t_resource.id == id_resource).select().first()
    row.update_record(f_is_verificado=False)

    course = db.t_comments.insert(
        recurso = id_resource,
        texto = comentario,
    )

    redirect(URL('display_resources'))  
    #return locals()


def display_file_form():
    record = db.t_file(request.args(0))
    form = SQLFORM(db.t_file, record, deletable=True,
                  upload=URL('download'))

    if form.process(onvalidation=validar_form_archivo).accepted:
       response.flash = 'form accepted'
    elif form.errors:
       response.flash = 'form has errors'
    return dict(form=form)

def display_files():
    form = SQLFORM.smartgrid(db.t_file,onupdate=auth.archive)
    return locals()
    
@auth.requires_login()
def program_manage():
    return dict()

@auth.requires_login()
def program_creator():
    program_type = request.post_vars['program_type']
    program_name = ""

    if (program_type == "carreraLarga"):
        program_name = "Carrera Larga"
    elif (program_type == "carreraCorta"):
        program_name = "Carrera Corta"
    elif (program_type == "postgrado"):
        program_name = "Postgrado"
    elif (program_type == "diplomado"):
        program_name = "Diplomado"
    elif (program_type == "curso"):
        program_name = "Curso"
    elif (program_type == "programa"):
        program_name = "Programa"

    data = {'program_type': program_type, 'program_name': program_name}
    return data

@auth.requires_login()
def program_creator_courses():
    program_type = request.get_vars['type']
    duration = int(request.post_vars['years'])
    modality = request.post_vars['modality']
    name = request.post_vars['name']
    code = request.post_vars['code']

   # nulo = db(db.t_course.f_code == code).select()
   # if nulo:

   # print(nulo)
   # print("HOLA")

    # Getting size
    size = 0
    if (modality=='trimestral'):
        size = 3
    elif (modality=='semestral'):
        size = 6
    elif (modality=='anual'):
        size = 12

    # Create Database Entries
    if (program_type in ('carreraLarga', 'carreraCorta', 'postgrado')):
        # Nivel de anidacion I
        level_one_id = db.t_program.insert(
            f_name = name,
            f_modality = modality,
            f_code = code,
            f_duration = duration,
            f_level = 0
        )

        complete_duration = int(duration)*12/size

        programsIDs = list()

        for i in range(0, complete_duration):
            level_two_id = db.t_program.insert(
                f_name = name + ' - ' + modality + ' - ' + str(i),
                f_modality = None,
                f_code = code,
                f_duration = size,
                f_level = 1
            )

            db.t_has_program.insert(
                f_program_a = level_one_id,
                f_program_b = level_two_id
            )

            programsIDs.append(level_two_id)
    elif (program_type in ('diplomado', 'curso') ):
        complete_duration = int(duration)*12/size

        # Nivel de anidacion 0 
        level_one_id = db.t_program.insert(
            f_name = name,
            f_modality = modality,
            f_code = code,
            f_duration = duration
        )
        programsIDs.append(level_one_id)
    elif (program_type == 'programa'):
        # Nivel de anidacion variable
        complete_duration = int(duration)*12/size
        pass

    return {'duration': complete_duration, 'size': size, 'modality' : modality, 'programs': programsIDs}

@auth.requires_login()
def save_course():
    program = request.post_vars['program']
    course_code = request.post_vars['course_code']
    course_name = request.post_vars['course_name']
    message = ''
    status = False
    
    # DB Inserts
    validate = False
    sanity_check_course = db(db.t_course.f_code == course_code).select()

    for row in sanity_check_course:
        validate = True

    if ( not validate ):
        print("This case is triggered")
        course = db.t_course.insert(
            f_code = course_code,
            f_name = course_name,
        )
    else:
        course = sanity_check_course[0]

    has_course = db.t_has_course.insert(
        f_program_has = program,
        f_course_has = course
    );

    status = has_course != None and course != None

    data = {'course': course, 'has_course': has_course, 'course_name': course_name, 'status': status}
    return data


@auth.requires_login()
def project_manage():
    return dict()


@auth.requires_login()
def project_asign_responsibles():
    codigo = request.get_vars['codigo']
    data = list()
    courses = db(db.t_has_course.f_program_has.belongs(db.t_program.f_code == codigo)).select()
    for course in courses:
        data.append(db(db.t_course.id == course.f_course_has).select())
    return dict(courses_ = data)


@auth.requires_login()
def get_user_names():
    usernames = db(db.auth_user).select(db.auth_user.first_name, db.auth_user.last_name)
    names = '';
    for name in usernames:
        names = names + str(name['auth_user.first_name']) + ' ' + str(name['auth_user.last_name']) + '|'
    data = {'usernames': names}
    return data

@auth.requires_login()
def profesor():
    return dict()

@auth.requires_login()
def disenador():
    return dict()


