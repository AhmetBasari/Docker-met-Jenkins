#!/bin/bash
yum update -y
yum install -y python3 python3-pip

# Install Flask and MySQL Connector
pip3 install flask mysql-connector-python

# Create the Bookstore API
cat <<EOF > /home/ec2-user/bookstore-api.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Bookstore API!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
EOF

# Start the Bookstore API
nohup python3 /home/ec2-user/bookstore-api.py &
