import cherrypy
'''
goal
servers single form at frontend
receives link from user
    validate etc
returns file.
'''

conf = {
    '/':{
        'tools.staticdir.on' :True,
        'tools.staticdir.dir':'/home/mwachala/Desktop/booker/server/static',
        'tools.staticdir.index':'home.html'
        }
}

class Server(object):
    pass

if __name__ == "__main__":
    cherrypy.quickstart(Server(), config=conf)
