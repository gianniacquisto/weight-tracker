FROM python:3.12-slim-bookworm
ADD requirements.txt .
RUN pip install -r requirements.txt
ADD app.py .
EXPOSE 8000
ENTRYPOINT ["uvicorn", "app:app"]