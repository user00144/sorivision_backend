from fastapi import APIRouter, Query
from models.client_models import ContentDetailResponse, DeviceInfoResponse, GPSTraceResponse, CalendarByDayResponse
from services.client_services.content_detail_service import get_content_detail
from services.client_services.device_info_service import get_device_info
from services.client_services.gps_trace_service import get_recent_gps_trace
from services.client_services.emergency_service import get_emergency_image_urls
from services.client_services.preview_image_service import get_preview_images
from services.client_services.calendar_service import get_calendar_info
from typing import List

router = APIRouter(tags=["Client"])

@router.get("/get_content_byid", response_model=ContentDetailResponse)
async def get_content_by_id_api(
    device_id: str = Query(..., description="디바이스 ID"),
    contents_id: str = Query(..., description="콘텐츠 ID")
):
    result = await get_content_detail(device_id, contents_id)

    return ContentDetailResponse(**result)

@router.get("/device_info", response_model=DeviceInfoResponse)
async def device_info(device_id: str = Query(..., description="디바이스 ID")):
    """
    기기 ID를 기준으로 사용자 정보를 반환하는 API
    """
    result = await get_device_info(device_id)

    return DeviceInfoResponse(**result)

@router.get("/gps_trace", response_model= GPSTraceResponse)
async def gps_trace(device_id: str = Query(..., description="조회할 디바이스 ID")):
    """
    보호자가 특정 device_id에 대해 최근 1시간 이내 GPS 위치 타임라인을 조회
    """
    gps_data =  await get_recent_gps_trace(device_id)
    return {"gps": gps_data}

@router.get("/get_emergency_imglist")
async def get_emergency_imglist(
    device_id: str = Query(..., description="디바이스 ID"),
    emergency_id: str = Query(..., description="비상 상황 ID")
):
    """
    비상 상황의 이미지 URL 목록을 조회하는 API
    """
    try:
        image_urls = await get_emergency_image_urls(device_id, emergency_id)
        return {
            "image_urls": image_urls
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
    
@router.get("/get_preview_images")
async def get_preview_images_api(
    device_id: str = Query(..., description="디바이스 ID"),
    date: str = Query(..., description="조회한 날짜 (YYYY-MM-DD)")
):
    result = await get_preview_images(device_id, date)

    return result

@router.get("/get_calendar_info", response_model=CalendarByDayResponse)
async def get_calendar_info_api(
    device_id: str = Query(..., description="디바이스 ID"),
    year: int = Query(..., description="연도"),
    month : int = Query(..., description="월")
):
    result = await get_calendar_info(device_id, year, month)
    return CalendarByDayResponse(**result)

