import requests
from flask import Flask,render_template,url_for
from flask import request as req


app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def Index():
    return render_template("index.html")

@app.route("/Summarize", methods=["GET", "POST"])
def Summarize():
    if req.method == "POST":
        try:
            API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
            headers = {"Authorization": "Bearer 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"}

            data = req.form["data"]

            maxL = int(req.form["maxL"])
            minL = maxL // 4

            def query(payload):
                response = requests.post(API_URL, headers=headers, json=payload)
                return response.json()

            output = query({
                "inputs": data,
                "parameters": {"min_length": minL, "max_length": maxL},
            })

            # Print the entire dictionary
            print(output)

            # Check if the output is a list and non-empty before accessing its elements
            if isinstance(output, list) and output:
                summary_text = output[0].get("summary_text", "No summary available")
            else:
                summary_text = "No summary available"

            return render_template("index.html", result=summary_text)
        except Exception as e:
            # Log the exception for debugging purposes
            print(e)
            return "An error occurred while summarizing the data."
    else:
        return render_template("index.html")
