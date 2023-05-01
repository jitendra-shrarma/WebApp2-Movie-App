import os
import jinja2
import webapp2
from google.appengine.ext import ndb

from models import Movie

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


def url_for(name, **kwargs):
    return webapp2.uri_for(name, **kwargs)


# Add the url_for function to the Jinja2 environment as a global variable
jinja_env.globals.update(url_for=url_for)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        movies = Movie.query().order(Movie.title).fetch()
        template = jinja_env.get_template("movie_list.html")
        self.response.out.write(template.render({"movies": movies}))


class AddMovieHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template("add_movie.html")
        self.response.out.write(template.render())

    def post(self):
        movie = Movie(
            title=self.request.get("title"),
            genre=self.request.get("genre"),
            year=int(self.request.get("year")),
            director=self.request.get("director"),
        )
        movie.put()
        self.redirect("/")


class EditMovieHandler(webapp2.RequestHandler):
    def get(self, movie_id):
        movie = ndb.Key(Movie, int(movie_id)).get()
        template = jinja_env.get_template("edit_movie.html")
        self.response.out.write(template.render({"movie": movie}))

    def post(self, movie_id):
        movie = ndb.Key(Movie, int(movie_id)).get()
        movie.title = self.request.get("title")
        movie.genre = self.request.get("genre")
        movie.year = int(self.request.get("year"))
        movie.director = self.request.get("director")
        movie.put()
        self.redirect("/")


class SearchMovieHandler(webapp2.RequestHandler):
    def get(self):
        query = self.request.get("query")
        movies = Movie.query(
            ndb.OR(
                Movie.title._IN([query]),
                Movie.genre._IN([query]),
                Movie.director._IN([query]),
            )
        ).fetch()
        template = jinja_env.get_template("movie_list.html")
        self.response.out.write(template.render({"movies": movies}))
