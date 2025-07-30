FROM quay.io/centos/centos:stream9

RUN dnf install -y python3.9 python3-pip

WORKDIR /myportfolio

COPY . .
COPY app/.env /myportfolio/app/.env
#COPY requirements.txt .
# Add wait-for-it.sh
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

RUN pip3 install -r requirements.txt

# Wait for MySQL before starting Flask
CMD ["./wait-for-it.sh", "db:3306", "--", "flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

