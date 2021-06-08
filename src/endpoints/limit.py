from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from fastapi.routing import APIRouter
from starlette.requests import Request
from starlette.responses import Response

from src.apikey import ApiKey

API_KEY_HEADER = 'X-API-KEY'

router = APIRouter()
api_key_db = ApiKey()


@router.get("/limit")
async def limit(request: Request) -> Response:
    api_key = request.headers.get(API_KEY_HEADER)

    if not api_key:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="X-API-KEY header not found",
        )

    result = await api_key_db.find_api_key(api_key)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="ApiKey not valid",
        )

    api_key_id = result['id']
    count_api_key_usage = await api_key_db.count_api_key_usage(datetime.now(), api_key_id)

    if count_api_key_usage >= 10:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail="ApiKey rate limit exceeded",
        )

    await api_key_db.update_api_key_usage(api_key_id)

    return Response(status_code=HTTPStatus.OK)
