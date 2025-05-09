from core.firebase import db

def get_device_ref(device_id : str):
    """
    디바이스 document 참조 변환
    """
    return db.collection("devices").document(device_id)

def get_contents_ref(device_id : str):
    """
    디바이스 하위 contents 컬렉션 참조 반환
    """
    return get_device_ref(device_id).collection("contents")

def get_location_ref(device_id : str):
    """
    디바이스 하위 locations 컬렉션 참조 반환 (gps용)
    """
    return get_device_ref(device_id).collection("locations")

def get_emergency_ref(device_id: str):
    """
    디바이스 하위 emergency 컬렉션 참조 반환
    """
    return get_device_ref(device_id).collection("emergency")



