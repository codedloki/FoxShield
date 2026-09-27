# 1. Use the official uv Docker image
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# 2. Set working directory (Fkt ekdaach sufficient ahe)
WORKDIR /app

# 3. Environment variables for faster, reproducible installs
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-hin poppler-utils && rm -rf /var/lib/apt/lists/*

# 4. Copy dependency files FIRST (Docker Layer Caching sathi he crucial ahe!)
COPY pyproject.toml uv.lock ./

# 5. Install dependencies using uv sync (without installing the project yet)
RUN uv sync --frozen --no-install-project

# 6. CRITICAL FIX: Download Spacy model using venv's Python directly.
# 'uv run' vaparla tar to project build karaycha prayatna karto, je fail hote karan source code ajun copy zala nahiye.
# Direct venv python vaprun he bypass karto.
RUN /app/.venv/bin/python -m spacy download en_core_web_lg

# 7. NOW copy the rest of the application code
COPY . .

# 8. Add the virtual environment to the PATH so Streamlit/uv can find it
ENV PATH="/app/.venv/bin:$PATH"

# 9. Expose Streamlit port
EXPOSE 8501

# 10. Run the Streamlit app (Aata source code aslyamule 'uv run' perfectly kaam karel)
CMD ["uv", "run", "streamlit", "run", "src/foxshield/app.py", "--server.port", "8501", "--server.address", "0.0.0.0", "--server.headless", "true"]
