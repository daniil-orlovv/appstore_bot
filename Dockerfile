FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["python", "main.py"]
