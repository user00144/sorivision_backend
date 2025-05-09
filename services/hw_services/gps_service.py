from core.firebase_utils import get_device_ref, get_location_ref
from fastapi import HTTPException
from datetime import datetime

async def save_gps_location(device_id: str, lat: float, lon: float):
    """
    주어진 device_id의 디바이스 문서 하위에 위치 정보 저장
    """
    device_ref = get_device_ref(device_id)
    doc = device_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="디바이스가 존재하지 않습니다")

    location_ref = get_location_ref(device_id).document()
    location_ref.set({
        "lat" : lat,
        "lon" : lon,
        "timestamp": datetime.utcnow()
    })
    return True
