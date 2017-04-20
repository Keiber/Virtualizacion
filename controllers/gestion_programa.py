
@auth.requires_login()
def project_creator():
	codigo = request.post_vars['codigo']
	nobre = request.post_vars['nombre']

	programa = (db(db.t_program.f_code == codigo and db.t_program.f_level == 0).select())[0]
	progress = 'Iniciado'

	result = db.t_project.insert(
        f_program = programa,
        f_progress = progress
    )

	if result != None:
		return dict(status = True)
	return dict(status = False)