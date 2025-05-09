from core.firebase_utils import get_contents_ref
from fastapi import HTTPException

async def get_preview_images(device_id: str, date: str) -> dict:
    """"
    id_list 기반으로(날짜) 컨텐츠 이미지 url 가져오기 (이중 리스트 형태로 반환)
    """

    contents_ref = get_contents_ref(device_id)
    docs = contents_ref.stream()

    ids, urls = zip(*[
        (doc.id, data.get("image_url", ""))
        for doc in docs
        if (data := doc.to_dict()).get("created_at") and data.get("created_at").split("T")[0] == date
    ]) if docs else ([], [])

    if not ids:
        raise HTTPException(status_code=404, detail="해당 날짜에 컨텐츠가 없습니다.")
    
    return {
        "contents_list_image": [list(ids,), list(urls)]
    }
