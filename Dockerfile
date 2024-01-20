FROM python:3.12-slim-bookworm
# Or any preferred Python version.
ADD app.py .
RUN pip install fastapi uvicorn
# CMD [“uvicorn”, “app:app”] 
CMD [“python”, “./app.py”]
# Or enter the name of your unique directory and parameter set.