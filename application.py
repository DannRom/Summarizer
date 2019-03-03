from flask import Flask, render_template, request, abort
from werkzeug.exceptions import HTTPException, default_exceptions
from time import perf_counter
from summarize import sumTarget, sumLimit
import os

# Web app
app = Flask(__name__)


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Handle requests for / via GET (and POST)"""
    return render_template("index.html")


@app.route("/file_summary", methods=["POST"])
def file_summary():
    """Handle requests for /file_summary via POST"""

    # Check if file is valid
    if not request.files["file"]:
        abort(400, "missing file")
    try:
        # Get article
        article = request.files["file"].read().decode("utf-8")
    except Exception:
        abort(400, "invalid file")

    if request.form.get("sumTarget"):

        target = request.form.get("target")
        result = sumTarget(article, target)

    elif request.form.get("sumLimit"):

        try:
            limit = int(request.form.get("limit"))
            if limit < 0:
                abort(400, "must be a positive whole number")
        except:
            abort(400, "must be a positive whole number")

        result = sumLimit(article, limit)

    return render_template("summary.html", article=article, result=result)


@app.route("/text_summary", methods=["POST"])
def text_summary():
    """Handles request for /text_summary via POST"""

    # Check if text is present
    if not request.form.get("text"):
        abort(400, "missing article text")

    # Check target range
    target = request.form.get("target")

    # Circumvents bug [1]
    content = request.form.get("text")
    f = open("summary.txt","w+")
    f.write(content)
    f.close()
    f = open("summary.txt", "r")
    article = f.read()
    f.close()
    if os.path.isfile("summary.txt"):
        os.remove("summary.txt")

    if request.form.get("sumTarget"):

        target = request.form.get("target")
        result = sumTarget(article, target)

    elif request.form.get("sumLimit"):

        try:
            limit = int(request.form.get("limit"))
            if limit < 0:
                abort(400, "must be a positive whole number")
        except:
            abort(400, "must be a positive whole number")

        result = sumLimit(article, limit)

    return render_template("summary.html", article=article, result=result)


@app.route("/about", methods=["GET", "POST"])
def about():
    """Handles requesr for /about via POST"""
    return render_template("about.html")


@app.errorhandler(HTTPException)
def errorhandler(error):
    """Handle errors"""
    return render_template("error.html", error=error), error.code


# https://github.com/pallets/flask/pull/2314
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

"""Bug [1]"""
# All this could be done in one line, as it is done with
# the /file_summary route. Yet for whatever reason the text
# retrieved cannot be summarized. Printing the text appears fine;
# creating a new file containing the text (as done below) is fine.
# Yet normal manipulation of the string does not work otherwise.
# The string seems to have omitted \n\n for \n, therefore
# creating an issue with summarize() which divides
# the text into paragraphs using .split("\n\n").
# Also .replace("\n", "\n\n") is not an adequate solution,
# since the original '\n' in the text are preserved.