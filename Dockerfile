FROM python:3.9-slim

# 设置环境变量
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY models /app/models
COPY app.py /app

 


# 推荐方式（Python 直接启动）
#CMD ["python", "app.py"]

# 或者生产环境使用
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "app:app"]