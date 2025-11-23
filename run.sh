#!/bin/bash

# EC2 메타데이터 토큰 요청(IMDSv2)
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600" -s)

# 퍼블릭 IP 가져오기
PUBLIC_IP=$(curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/public-ipv4 -s)

echo "======================================="
echo "🚀 Streamlit 서버 시작!"
echo "🌍 접속 주소 : http://$PUBLIC_IP:8501"
echo "======================================="

# Streamlit 실행
streamlit run server/app/main.py --server.address 0.0.0.0 --server.port 8501
