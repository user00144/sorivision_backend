import os
import json
import aiohttp
from fastapi import HTTPException
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from firebase_admin import firestore

# 서비스 계정 JSON 경로
SERVICE_ACCOUNT_FILE = os.getenv("FIREBASE_CREDENTIAL_PATH")
PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging"]

def get_access_token():
    """Firebase 서비스 계정을 사용하여 액세스 토큰을 가져옵니다."""
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    credentials.refresh(Request())
    return credentials.token

async def send_emergency_push(device_id: str, emergency_id: str):
    """
    FCM HTTP v1 API를 사용하여 비상 상황 푸시 알림을 전송합니다.
    
    Args:
        device_id (str): 디바이스 ID
        emergency_id (str): 비상 상황 ID
    """
    if not PROJECT_ID:
        raise HTTPException(status_code=500, detail="FIREBASE_PROJECT_ID 환경변수가 설정되지 않았습니다.")

    # 디바이스 정보 조회
    db = firestore.client()
    device_doc = db.collection('devices').where('device_id', '==', device_id).limit(1).get()
    
    if not device_doc:
        raise HTTPException(status_code=404, detail="디바이스를 찾을 수 없습니다.")
    
    device_data = device_doc[0].to_dict()
    fcm_token = device_data.get('fcm_token')
    
    if not fcm_token:
        raise HTTPException(status_code=400, detail="디바이스의 FCM 토큰이 등록되지 않았습니다.")

    # FCM 메시지 전송
    access_token = get_access_token()
    url = f"https://fcm.googleapis.com/v1/projects/{PROJECT_ID}/messages:send"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    message = {
        "message": {
            "token": fcm_token,
            "notification": {
                "title": "🚨 비상 상황 발생",
                "body": f"디바이스 {device_id}에서 긴급 상황이 발생했습니다."
            },
            "data": {
                "device_id": device_id,
                "emergency_id": emergency_id
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(message)) as resp:
            if resp.status != 200:
                error = await resp.text()
                raise HTTPException(status_code=resp.status, detail=f"FCM 전송 실패: {error}")
            return {"status": "success"}
