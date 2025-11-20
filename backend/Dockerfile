FROM python:3.13.1-slim


# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application into the container.
# /backend/docker에서의 .이라 backend 디렉토리를 가리킨다.
# 내가 backend폴더라고 이름지었지만, 결국 복사는 컨테이너 속 /app폴더로 이동한다.
#COPY . /app
COPY . /app/backend


# Install the application dependencies.
# -> WORKDIR /app로 이동한 상태. 여기에 main.py가 있다.
#WORKDIR /app
WORKDIR /app/backend
RUN uv sync --frozen --no-cache

# Run the application.
#CMD ["/app/.venv/bin/fastapi", "run", "app/main.py", "--port", "80", "--host", "0.0.0.0"]
#CMD ["/app/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]
CMD ["/app/backend/.venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]
