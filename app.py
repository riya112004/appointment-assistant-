import logging

from flask import Flask, Response, request

from analysis import AnalysisError, analyze_complaint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return Response(
            "Send POST with form field 'message' (or JSON) to get an analysis.",
            mimetype="text/plain",
        )

    if request.is_json:
        payload = request.get_json(silent=True) or {}
        message = payload.get("message", "")
    else:
        message = request.form.get("message", "")

    message = message.strip() if isinstance(message, str) else ""
    if not message:
        return Response(
            "Please enter your message.", status=400, mimetype="text/plain"
        )

    try:
        analysis = analyze_complaint(message)
    except AnalysisError as exc:
        app.logger.error("Symptom analysis failed: %s", exc)
        return Response(
            "Analysis service is unavailable. Please try again later.",
            status=502,
            mimetype="text/plain",
        )

    body = (
        f"Detected Category: {analysis['detected_category']}\n"
        f"Suggested Specialty: {analysis['suggested_specialty']}"
    )
    return Response(body, mimetype="text/plain")


if __name__ == "__main__":
    app.logger.info("Starting Flask application.")
    app.run(debug=True)
