# ---------- STEP 1: Use official Python image ----------
FROM python:3.11-slim

# ---------- STEP 2: Set working directory ----------
WORKDIR /app

# ---------- STEP 3: Copy requirements ----------
COPY requirements.txt .

# ---------- STEP 4: Install dependencies ----------
RUN pip install --no-cache-dir -r requirements.txt

# ---------- STEP 5: Copy the app ----------
COPY ./app ./app

# ---------- STEP 6: Expose port ----------
EXPOSE 8000

# ---------- STEP 7: Run FastAPI with Uvicorn ----------
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]