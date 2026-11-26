import logging

from flask import Flask, Response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = Flask(__name__)

FIXED_RESPONSE = (
    "Detected Category: Gastrointestinal and systemic symptoms\n"
    "Suggested Specialty: General Practice"
)


@app.route("/", methods=["GET", "POST"])
def home():
    return Response(FIXED_RESPONSE, mimetype="text/plain")


if __name__ == "__main__":
    app.logger.info("Starting Flask application.")
    app.run(debug=True)
