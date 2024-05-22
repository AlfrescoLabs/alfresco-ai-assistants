FROM langchain/langchain

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

RUN mkdir -p static
COPY static/*.png static

COPY alfresco_ai_assistant.py .
COPY alfresco_api.py .
COPY commons.py .
COPY report_writer.py .

EXPOSE 8504

HEALTHCHECK CMD curl --fail http://localhost:8504/_stcore/health

ENTRYPOINT ["streamlit", "run", "alfresco_ai_assistant.py", "--server.port=8504", "--server.address=0.0.0.0"]
