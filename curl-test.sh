#!/bin/bash

BASE_URL="http://localhost:5000/api/timeline_post"
RANDOM_STR=$(openssl rand -hex 4)
NAME="TestUser"
EMAIL="testuser${RANDOM_STR}@example.com"
CONTENT="Test content ${RANDOM_STR}"

POST_RESPONSE=$(curl -s -X POST $BASE_URL -d "name=${NAME}&email=${EMAIL}&content=${CONTENT}")
echo "$POST_RESPONSE"

POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)

if [ -z "$POST_ID" ]; then
    exit 1
fi

GET_RESPONSE=$(curl -s $BASE_URL)

if echo "$GET_RESPONSE" | grep -q "$CONTENT"; then
    echo "Success"
else
    echo "Failure"
    exit 1
fi

