@request.restful()
def api():

    def GET(*args, **vars):
        return dict(nombre = 'Moisés')

    def POST(*args, **vars):
        return dict(nombre = 'Moisés')

    def PUT(*args, **vars):
        return dict()

    def DELETE(*args, **vars):
        return dict()

    return locals()


@request.restful()
def user():
    def GET(id):
        #raise HTTP(440)
        return dict()

    def GET(*args, **vars):
        return dict(params = len(args))

    return locals()