from fastapi import Header, HTTPException
from firebase_admin import auth, exceptions
from typing import Annotated # 타입 힌트 유지

async def get_current_user_uid(authorization: Annotated[str, Header()]): # 1. Header() 안의 None 제거
    """
    HTTP 헤더에서 ID 토큰을 추출하고 검증하여, 유효한 경우 사용자의 UID를 반환합니다.
    """
    
    # 2. 대신 함수 인자 자체에 기본값 None을 설정 (오류 해결)
    if authorization is None or not authorization.startswith("Bearer "): 
        raise HTTPException(
            status_code=401, 
            detail="인증 토큰(Authorization: Bearer <token>)이 필요합니다."
        )

    # ... (나머지 로직은 그대로 유지)
    # 'Bearer ' 접두사 제거
    id_token = authorization.split("Bearer ")[-1]
    
    try:
        # ... (Firebase 검증 로직)
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token["uid"]

    except exceptions.FirebaseError:
        raise HTTPException(
            status_code=401, 
            detail="유효하지 않거나 만료된 토큰입니다. 재로그인이 필요합니다."
        )