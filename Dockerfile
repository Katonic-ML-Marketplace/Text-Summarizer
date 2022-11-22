FROM python:3.8.2-slim

RUN mkdir -p static/css static/js static/img templates

COPY app.py .
COPY nltk_summarization.py .
COPY spacy_summarization.py .
COPY spacy_summarizer.py .
COPY static/img/logo.png static/img/.
COPY static/css/custom.css static/css/.
COPY static/css/materialize.css static/css/.
COPY static/css/materialize.min.css static/css/.
COPY static/js/init.js static/js/.
COPY static/js/materialize.js static/js/.
COPY static/js/materialize.min.js static/js/.
COPY templates/index.html templates/.
COPY templates/compare_summary.html templates/.
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

CMD python app.py --server.port=8050 --server.address=0.0.0.0 --logger.level error
