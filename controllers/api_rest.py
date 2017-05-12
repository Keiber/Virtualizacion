#GENERAL FUNCTIONS

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

#API_REST

#GETS
@auth.requires_login()
@request.restful()
def get_users():
    def GET(*args, **vars):
        usuarios_sistema = db(db.t_usuario).select()
        return dict(users = usuarios_sistema, length_users = len(usuarios_sistema))
    return locals()

@auth.requires_login()
@request.restful()
def get_programs():
    def GET(*args, **vars):
        projects = db(db.t_project).select()  
        programs = db(db.t_program).select()
        data = list()
        cont_aux = 0
        for fila in projects:
            for programa in programs:                
                if fila.f_program.id == programa.id:
                    data.append(dict(programa = programa, virtualizado = 1, progreso = fila.f_progress))

        for aux in programs:
            for virt in data:
                if aux.id == virt["programa"].id:
                    cont_aux = 1
                    pass
            if cont_aux == 0:
                data.append(dict(programa = aux, virtualizado = 0, progreso = "0%"))
        return dict(data = data)
    return locals()

@auth.requires_login()
@request.restful()
def get_notifications():
    def GET(*args, **vars):
        notificacion = db(db.t_notification.f_usuario_b == auth.user.id).select()
        return dict(notification = notificacion, length_notification = len(notificacion) )
    return locals()

@auth.requires_login()
@request.restful()     # Revisar - KEIBER - EFRA
def get_files():
    def GET(*args, **vars): 
        files = db(db.t_file).select()
        return dict(users = files, length_users = len(files))

    def POST(*args, **vars):
        return dict()
    return locals()

@auth.requires_login()
@request.restful()     
def get_project_responsibles():
    def GET(codigo_request): 
        codigo = codigo_request
        data = list()
        courses = db(db.t_has_course.f_program_has.belongs(db.t_program.f_code == codigo)).select()
        for course in courses:
            data.append(db(db.t_course.id == course.f_course_has).select())
        return dict(courses_ = data)

    def POST(*args, **vars):
        return dict()
    return locals()


#GETS - REVISION -----------------------------------------------------------------------------
@auth.requires_login()
@request.restful()
def get_planillas(): #KEIBER - EFRA   - REVISAR SI CAMBIARÁ A SOLO BUSQUEDA EN BD
    def GET(*args, **vars):
        form = SQLFORM.smartgrid(db.t_resource, constraints = dict(t_resource = db.t_resource.f_is_planilla == True),
            onupdate=auth.archive,
            deletable=False,
            editable=False,
            searchable=False,
            create=False,
            csv=False,
            showbuttontext=False)
        return locals()
    def POST(*args, **vars):
        return dict()
    return locals()

@auth.requires_login()
@request.restful()
def get_resources(): #KEIBER - EFRA  - REVISAR SI CAMBIARÁ A SOLO BUSQUEDA EN BD
    def GET(*args, **vars):
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
    def POST(*args, **vars):
        return dict()
    return locals()

#FIN GETS - REVISION ------------------------------------------------------------------------------------


# POST
@auth.requires_login()
@request.restful()
def create_notification():
    def GET(*args, **vars):
        return dict()
    def POST(user_receptor_request, titulo_request, contenido_request): #NOTA: ESTA REQUIERE UN AUTH 
        user_emisor, user_receptor, titulo, contenido = auth.user.id, user_receptor_request, titulo_request, contenido_request
        select = db(db.t_usuario.f_first_name == user_receptor).select()
        id_receptor = 0

        for row in select:
            id_receptor = row.id
        try:            
            db.t_notification.insert(
                f_usuario_a = user_emisor,
                f_usuario_b = id_receptor,
                f_tittle = titulo,
                f_viewed = False,
                f_content = contenido
                )             
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:
            db.commit()
            return dict(status = "200", msg= "Operación exitosa", contenido = "Se ha creado la notificación "+titulo+" correctamente")

    return locals()

@auth.requires_login()
@request.restful()
def create_user():
    def GET(*args, **vars):
        return dict()
    def POST(user_name, name, last_name, user_type, email, password): 
        #user_name, name, last_name, user_type, email, password = request.post_vars['user_name'],request.post_vars['name'], request.post_vars['last_name'], request.post_vars['user_type'], request.post_vars['email'], request.post_vars['password']
        try:
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
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = "Se ha creado el usuario "+user_name+" correctamente")
    return locals()

@auth.requires_login()
@request.restful()
def verificar_planillas():
    def GET(*args, **vars):        
        return dict()

    def POST(id_resource):
        try:
            row = db(db.t_resource.id == id_resource).select().first()
            row.update_record(f_is_verificado=True)
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = "Se ha actualizado el recurso a verificado")
    return locals()

#REVISAR ESTA ------------------------------------------------------
@auth.requires_login()
@request.restful()
def verificar_resources():
    def GET(*args, **vars):        
        return dict()

    def POST(id_resource):
        row = db(db.t_resource.id == id_resource).select().first()
        row.update_record(f_is_verificado=True)
        return dict()
    return locals()
#--------------------------------------------------------------------
@auth.requires_login()
@request.restful()
def desverificar_resources():
    def GET(*args, **vars):        
        return dict()

    def POST(id_resource, comment):
        try:
            comentario = comment
            row = db(db.t_resource.id == id_resource).select().first()
            row.update_record(f_is_verificado=False)

            course = db.t_comments.insert(
                recurso = id_resource,
                texto = comentario,
            )
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = "Se ha actualizado el recurso a desverificado")
    return locals()



@request.restful()
def insert_project():
    def GET(*args, **vars):        
        return dict()

    def POST(id_program):
        try:
            db.t_project.insert(
                f_program = id_program,
                f_progress = "0%"
            )
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = "Se ha insertado el proyecto exitosamente")
    return locals()

#@auth.requires_login()
#@request.restful()
#def create_program():
#    def GET(*args, **vars):
#        program_name = ""
#
#        if (program_type == "carreraLarga"):
#            program_name = "Carrera Larga"
#        elif (program_type == "carreraCorta"):
#            program_name = "Carrera Corta"
#        elif (program_type == "postgrado"):
#            program_name = "Postgrado"
#        elif (program_type == "diplomado"):
#            program_name = "Diplomado"
#        elif (program_type == "curso"):
#            program_name = "Curso"
#        elif (program_type == "programa"):
#            program_name = "Programa"
#        data = {'program_type': program_type, 'program_name': program_name}
#        return data   
#    def POST(program_type):
#        return dict()
#
#    return locals()

@auth.requires_login()
@request.restful()
def create_program_courses():
    def GET(*args, **vars):        
        return dict()

    def POST(program_type, duration, modality, name, code):

       # nulo = db(db.t_course.f_code == code).select()
       # if nulo:

       # print(nulo)
       # print("HOLA")

        # Getting size
        try:
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
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = dict(duration = complete_duration, size = size, modality = modality, programs = programsIDs))
    return locals()

@auth.requires_login()
@request.restful()
def save_course():
    def GET(*args, **vars):        
        return dict()

    def POST(program, course_code, course_name):
        try:
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
        except:
            db.rollback()
            return dict(status = "500", msg= "Error en el servidor", contenido = "Error en el servidor")
        else:    
            db.commit()     
            return dict(status = "200", msg= "Operación exitosa", contenido = dict(course = course, has_course = has_course, course_name = course_name, status= status))
    return locals()