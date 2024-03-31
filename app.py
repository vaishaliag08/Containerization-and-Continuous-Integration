from flask import Flask, request, jsonify, render_template
import score
import pickle
import warnings

warnings.filterwarnings("ignore")

## load the best classification model
with open("support_vector.pkl", "rb") as model_file:
    model = pickle.load(model_file)

app = Flask(__name__)

# Define a function for input validation
def is_valid_input(text, threshold):
    if not text.strip():
        return False, "Text input cannot be empty."
    try:
        threshold = float(threshold)
        if threshold < 0 or threshold > 1:
            raise ValueError("Threshold must be between 0 and 1.")
    except ValueError:
        return False, "Threshold must be a valid number between 0 and 1."
    return True, ""


@app.route("/", methods = ["GET", 'POST'])
def score_endpoint():
    ## get the data
    if request.method == "POST":
        text = request.form.get("text", "")
        threshold = float(request.form.get("threshold", ""))

        ## validate input
        is_valid, error_message = is_valid_input(text, threshold)
        if not is_valid:
            return jsonify({"error": error_message})

        ## get the prediction and propensity score from score function
        prediction, propensity = score.score(text, model, threshold)

        ## response in json format
        response = {
            "prediction" : int(prediction),
            "propensity" : float(propensity)
        }

        return jsonify(response)
    
    elif request.method == "GET":
        return render_template("index.html")

if __name__ == "__main__":
    ## Run the app
    app.run(debug = True)
