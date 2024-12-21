FROM  python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#copy product folder
# COPY ./limbo-dating-chat/matches_info /app/matches
COPY . .

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]
