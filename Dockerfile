
FROM python:3.10-slim


WORKDIR /app


COPY requirements.txt /app


RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

# Expose the port Flask will run on
EXPOSE 10000

# Set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "src/app.py"]
#CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-10000} src.app:app"]