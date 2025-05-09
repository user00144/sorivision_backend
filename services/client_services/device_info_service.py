from core.firebase_utils import get_device_ref
from fastapi import HTTPException

async def get_device_info(device_id: str) -> dict:
    """
    device_id 기반으로 device 정보 가져오기
    """
    device_ref = get_device_ref(device_id)
    doc = device_ref.get()

    if not doc.exists:
        raise HTTPException(status_code=404, detail="해당 디바이스를 찾을 수 없습니다")
    
    data =  doc.to_dict() 

    return {
        "user_name": data.get("user_name"),
        "guardian_name": data.get("guardian_name"),
        "guardian_phone": data.get("guardian_phone")
    }