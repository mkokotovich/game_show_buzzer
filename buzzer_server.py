import cherrypy

cherrypy.config.update('game_show_buzzer.config')

class BuzzerServer(object):
    teams = []
    @cherrypy.expose
    def index(self):
        msg =  '<meta http-equiv="refresh" content="1" />'
        if len(self.teams) == 0:
            msg += "<h1>Waiting for a team to buzz</h1>"
        else:
            msg += '<a href="/reset">Reset buzzer</a>'
            msg += "<h1>Teams have buzzed:</h1>"
            msg += "<br>".join("Team: " + t for t in self.teams)
        return msg


    @cherrypy.expose
    def reset(self):
        self.teams = []
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def buzz(self, team=None):
        msg = '<a href="/reset">Reset buzzer</a>'
        if team is not None and team not in self.teams:
            cherrypy.log("Team added : %s" % team)
            self.teams.append(team)
        msg += "<h1>Teams have buzzed:</h1>"
        msg += "<br>".join("Team: " + t for t in self.teams)
        return msg


cherrypy.quickstart(BuzzerServer())
