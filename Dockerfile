FROM python:3.8
COPY /app/ /app/
RUN pip install -r /app/requirements.txt
WORKDIR /app
CMD ["python", "qty_fin.py", "runserver", "9999"]