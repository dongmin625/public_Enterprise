# app/routers/users.py

from fastapi import APIRouter, HTTPException, Header
import firebase_admin
from firebase_admin import auth, exceptions 
from typing import Annotated, Optional # Optional은 Python 3.9 이하에서 Union[str, None] 대신 사용될 수 있습니다.

router = APIRouter(
    prefix="/users",
    tags=["사용자 인증"]
)

@router.get("/me")
async def verify_user_token(
    # [수정된 부분]
    # Header() 안에 None을 넣지 않고, 인자 자체에 '= None'을 설정합니다.
    # Optional[str]은 None을 허용하는 타입임을 명시합니다.
    authorization: Annotated[Optional[str], Header()] = None
):
    """
    클라이언트로부터 받은 Firebase ID 토큰을 검증하고, 유효한 경우 사용자 정보를 반환합니다.
    (클라이언트는 'Authorization: Bearer <ID_TOKEN>' 형태로 토큰을 전송해야 합니다.)
    """
    
    # 1. 인증 헤더 유효성 검사 (authorization이 None인지 체크)
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="유효하지 않거나 누락된 인증 헤더입니다.")

    # 'Bearer ' 접두사를 제거하고 순수 ID 토큰 추출
    id_token = authorization.split("Bearer ")[-1]
    
    # 2. Firebase Admin SDK를 사용하여 토큰 검증
    try:
        # 토큰을 검증하고 토큰에 포함된 클레임(정보)를 반환합니다.
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        
        # 3. UID를 사용하여 사용자 상세 정보 조회
        user = auth.get_user(uid)
        
        return {
            "message": "인증 성공",
            "uid": uid,
            "email": user.email,
            "display_name": user.display_name,
            "photo_url": user.photo_url,
            "is_email_verified": user.email_verified,
            "token_claims": decoded_token # 토큰의 모든 클레임(정보)
        }
        
    except exceptions.FirebaseError as e:
        # 토큰 만료, 잘못된 토큰 형식 등 Firebase 인증 관련 오류 처리
        print(f"❌ Firebase 인증 오류: {e}")
        raise HTTPException(status_code=401, detail="유효하지 않은 인증 토큰입니다. 재로그인이 필요합니다.")
        
    except Exception as e:
        print(f"❌ 서버 처리 중 오류: {e}")
        raise HTTPException(status_code=500, detail="서버 처리 중 알 수 없는 오류가 발생했습니다.")