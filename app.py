import logging

from flask import Flask, render_template, request

from analysis import AnalysisError, analyze_complaint

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    analysis = None
    error = None

    if request.method == "POST":
        app.logger.info("Received a symptom analysis request.")
        message = request.form.get("message", "").strip()
        if not message:
            error = "Please enter your symptoms."
            app.logger.warning("Analysis request rejected: empty message.")
        elif len(message) > 2000:
            error = "Please keep your message under 2,000 characters."
            app.logger.warning("Analysis request rejected: message exceeds the limit.")
        else:
            try:
                analysis = analyze_complaint(message)
            except AnalysisError as exc:
                error = str(exc)
                app.logger.error("Symptom analysis failed: %s", exc)
            else:
                app.logger.info("Symptom analysis completed successfully.")

    return render_template(
        "index.html",
        message=message,
        analysis=analysis,
        error=error,
    )


if __name__ == "__main__":
    app.logger.info("Starting Flask application.")
    app.run(debug=True)
