FROM python:3.12-slim

WORKDIR /usr/src/app
COPY ./gradio_app.py .
COPY ./model.pkl .
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "gradio_app.py"]