from firebase_admin import firestore
from fastapi import HTTPException

async def login_and_save_token(device_id: str, fcm_token: str) -> dict:
    db = firestore.client()

    query = db.collection("devices").where("device_id", "==", device_id).limit(1)
    docs = list(query.stream())

    if not docs:
        raise HTTPException(status_code=404, detail="디바이스를 찾을 수 없습니다.")

    device_ref = docs[0].reference
    device_ref.update({"fcm_token": fcm_token})

    return {"status": "success"}