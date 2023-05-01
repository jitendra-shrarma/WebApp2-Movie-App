from google.appengine.ext import ndb


class Movie(ndb.Model):
    title = ndb.StringProperty(required=True)
    genre = ndb.StringProperty(required=True)
    year = ndb.IntegerProperty(required=True)
    director = ndb.StringProperty(required=True)
