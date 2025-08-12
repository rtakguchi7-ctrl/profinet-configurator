FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask profi-dcp
EXPOSE 5000
CMD ["python", "app.py"]
