#!/bin/bash
yum update -y
yum install -y python3 python3-pip

pip3 install flask mysql-connector-python
cat <<EOF > /home/ec2-user/bookstore-api.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Bookstore API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
EOF

wget https://github.com/prometheus/prometheus/releases/download/v2.30.3/prometheus-2.30.3.linux-amd64.tar.gz
tar -xvf prometheus-2.30.3.linux-amd64.tar.gz
mv prometheus-2.30.3.linux-amd64 /usr/local/prometheus

cat <<EOF > /usr/local/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['localhost:80']
EOF

nohup python3 /home/ec2-user/bookstore-api.py &
nohup /usr/local/prometheus/prometheus --config.file=/usr/local/prometheus/prometheus.yml &
