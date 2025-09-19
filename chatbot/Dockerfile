FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV=production
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app", "--workers", "3"]
