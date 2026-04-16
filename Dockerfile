# ใช้ Python รุ่นที่เบาและเสถียร
FROM python:3.9-slim

# ตั้งค่าโฟลเดอร์ทำงานใน Container
WORKDIR /app

# ก๊อปปี้ไฟล์ requirements และติดตั้ง Library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ก๊อปปี้โค้ดทั้งหมด (app.py) เข้าไปใน Container
COPY . .

# เปิดพอร์ต 8080 ตามที่เราเขียนไว้ในโค้ด
EXPOSE 8080

# สั่งรันแอปพลิเคชัน
CMD ["ddtrace-run", "python", "app.py"]