import time
from urllib.request import urlopen

import en_core_web_sm
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
from flask import request
from gensim.summarization import summarize
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer

from nltk_summarization import nltk_summarizer
from spacy_summarization import text_summarizer

nlp = en_core_web_sm.load()
app = Flask(__name__)


# Sumy
def sumy_summary(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = " ".join(summary_list)
    return result


# Reading Time
def readingTime(mytext):
    total_words = len([token.text for token in nlp(mytext)])
    estimatedTime = total_words / 200.0
    return estimatedTime


# Fetch Text From Url
def get_text(url):
    page = urlopen(url)
    soup = BeautifulSoup(page)
    fetched_text = " ".join(map(lambda p: p.text, soup.find_all("p")))
    return fetched_text


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/index/analyze", methods=["GET", "POST"])
def analyze():
    start = time.time()
    if request.method == "POST":
        rawtext = request.form["rawtext"]
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end - start
    return render_template(
        "index.html",
        ctext=rawtext,
        final_summary=final_summary,
        final_time=final_time,
        final_reading_time=final_reading_time,
        summary_reading_time=summary_reading_time,
    )


@app.route("/index/analyze_url", methods=["GET", "POST"])
def analyze_url():
    start = time.time()
    if request.method == "POST":
        raw_url = request.form["raw_url"]
        rawtext = get_text(raw_url)
        final_reading_time = readingTime(rawtext)
        final_summary = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary)
        end = time.time()
        final_time = end - start
    return render_template(
        "index.html",
        ctext=rawtext,
        final_summary=final_summary,
        final_time=final_time,
        final_reading_time=final_reading_time,
        summary_reading_time=summary_reading_time,
    )


@app.route("/index/compare_summary")
def compare_summary():
    print("compare_summary", request.method)
    return render_template("compare_summary.html")


@app.route("/index/comparer", methods=["GET", "POST"])
def comparer():
    print(request.method)
    start = time.time()
    if request.method == "POST":
        rawtext = request.form["rawtext"]
        final_reading_time = readingTime(rawtext)
        final_summary_spacy = text_summarizer(rawtext)
        summary_reading_time = readingTime(final_summary_spacy)
        # Gensim Summarizer
        final_summary_gensim = summarize(rawtext)
        summary_reading_time_gensim = readingTime(final_summary_gensim)
        # NLTK
        final_summary_nltk = nltk_summarizer(rawtext)
        summary_reading_time_nltk = readingTime(final_summary_nltk)
        # Sumy
        final_summary_sumy = sumy_summary(rawtext)
        summary_reading_time_sumy = readingTime(final_summary_sumy)

        end = time.time()
        final_time = end - start
    return render_template(
        "compare_summary.html",
        ctext=rawtext,
        final_summary_spacy=final_summary_spacy,
        final_summary_gensim=final_summary_gensim,
        final_summary_nltk=final_summary_nltk,
        final_time=final_time,
        final_reading_time=final_reading_time,
        summary_reading_time=summary_reading_time,
        summary_reading_time_gensim=summary_reading_time_gensim,
        final_summary_sumy=final_summary_sumy,
        summary_reading_time_sumy=summary_reading_time_sumy,
        summary_reading_time_nltk=summary_reading_time_nltk,
    )


@app.route("/index/about")
def about():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
