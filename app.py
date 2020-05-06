from flask import Flask, send_from_directory, render_template, request, abort
from waitress import serve
from src.models.movie_recommend import recommender
from src.utils_mr import validate_input

app = Flask(__name__, static_url_path="/static")

@app.route("/")
def index():
    """Return the main page."""
    return send_from_directory("static", "index_mr.html")

@app.route("/get_results", methods=["POST"])
def get_results():
    """ Recommend the movies to a user by input the userID. """
    data = request.form
    print(data)

    test_value, errors = validate_input(data)

    if not errors:
        recommend_movies = recommender(test_value)
        return render_template("results_mr.html", recommend_movies=recommend_movies)
    else:
        return abort(400, errors)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
