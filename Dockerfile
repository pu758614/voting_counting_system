FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Create data directory for SQLite
RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/vote_system.db

EXPOSE 8080

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "wsgi:app"]