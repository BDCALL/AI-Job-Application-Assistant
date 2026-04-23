FROM python:3.10

WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000
EXPOSE 8501

# Run BOTH backend + frontend
CMD uvicorn backend:app --host 0.0.0.0 --port 8000 & \
    streamlit run app.py --server.port 8501 --server.address 0.0.0.0