import webapp2
from views import MainHandler, AddMovieHandler, EditMovieHandler, SearchMovieHandler


# Define app routes
app = webapp2.WSGIApplication(
    [
        ("/", MainHandler),
        ("/add", AddMovieHandler),
        ("/edit/(\d+)", EditMovieHandler),
        ("/search", SearchMovieHandler),
    ],
    debug=True
)
