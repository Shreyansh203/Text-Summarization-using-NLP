import requests
from flask import Flask, render_template, url_for, request as req, jsonify
from textblob import TextBlob
from collections import Counter
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

app = Flask(__name__)

# Define stopwords
stop_words = set(stopwords.words('english'))

@app.route("/", methods=["GET", "POST"])
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

            print(output)

            if isinstance(output, list) and output:
                summary_text = output[0].get("summary_text", "No summary available")
            else:
                summary_text = "No summary available"

            return render_template("index.html", result=summary_text)
        except Exception as e:
            print(e)
            return "An error occurred while summarizing the data."
    else:
        return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = req.json["data"]
        word_count = len(data.split())
        blob = TextBlob(data)
        sentiment_score = blob.sentiment.polarity
        if sentiment_score <= -0.5:
            sentiment = "The text seems very negative."
        elif sentiment_score <= 0:
            sentiment = "The text seems negative."
        elif sentiment_score <= 0.5:
            sentiment = "The text seems positive."
        else:
            sentiment = "The text seems very positive."
        words = [word for word in data.split() if word.lower() not in stop_words and word.isalpha()]
        keywords = [item[0] for item in Counter(words).most_common(5)]
        return jsonify({
            "word_count": word_count,
            "sentiment": sentiment,
            "keywords": keywords,
        })
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred during analysis."})

if __name__ == "__main__":
    app.run(debug=True)
