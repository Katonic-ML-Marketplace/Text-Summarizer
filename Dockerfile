FROM python:3.8.2-slim

COPY app.py .
COPY nltk_summarization.py .
COPY spacy_summarization.py .
COPY spacy_summarizer.py .
COPY static/img static/img
COPY static/css static/css
COPY static/js static/js
COPY templates templates
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm

CMD python app.py --server.port=8050 --server.address=0.0.0.0 --logger.level error
