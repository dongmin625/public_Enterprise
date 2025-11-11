// public-job-frontend/client/src/pages/PostingsPage.js

import React, { useState, useEffect } from "react";
import { useAuth } from "../AuthProvider"; // UID와 인증 상태를 가져오는 훅
import { signOut } from "firebase/auth";
import { auth } from "../firebase";

// 🚨 EC2 서버 주소를 사용합니다.
const FASTAPI_URL = "http://13.209.41.121:8000";

const PostingsPage = () => {
  const { currentUser } = useAuth();
  const [postings, setPostings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 로그아웃 처리 함수
  const handleLogout = async () => {
    try {
      await signOut(auth); // Firebase 로그아웃 요청
      // AuthProvider가 상태를 변경하여 자동으로 /login으로 리다이렉트됨
    } catch (error) {
      alert("로그아웃 실패: " + error.message);
    }
  };

  // ------------------------------------------------------------------
  // FastAPI 백엔드에서 인증 토큰을 사용하여 데이터 가져오기 (fetch 사용)
  // ------------------------------------------------------------------
  useEffect(() => {
    const fetchPostings = async () => {
      // 사용자가 없거나, 로딩 상태가 아닌 경우 (재실행 방지)
      if (!currentUser) {
        setLoading(false);
        return;
      }

      try {
        // 1. ID 토큰 발급 (Firebase Web SDK)
        const idToken = await currentUser.getIdToken();

        // 2. FastAPI 서버로 요청 보내기 (fetch 사용)
        const response = await fetch(`${FASTAPI_URL}/postings`, {
          method: "GET",
          headers: {
            // 토큰을 "Authorization: Bearer <token>" 형식으로 서버에 보냅니다.
            Authorization: `Bearer ${idToken}`,
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          // 응답 상태가 200이 아닌 경우 (401, 404, 500 등)
          if (response.status === 401) {
            // 401 Unauthorized 오류 시 로그아웃 처리
            await signOut(auth);
            throw new Error("인증 실패: 다시 로그인해주세요.");
          }
          throw new Error(
            `데이터를 가져오는 데 실패했습니다 (Status: ${response.status})`
          );
        }

        const data = await response.json();
        setPostings(data); // 데이터 상태 저장
      } catch (err) {
        // 네트워크 오류나 fetch 실패 오류 등을 처리
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPostings();
  }, [currentUser]); // currentUser 객체가 변경될 때마다 재실행

  // ------------------------------------------------------------------
  // 화면 렌더링
  // ------------------------------------------------------------------
  if (loading) return <p>공고 목록을 불러오는 중...</p>;

  // 에러 발생 시 로그아웃 버튼과 함께 오류 메시지 표시
  if (error)
    return (
      <div style={{ padding: "20px" }}>
        <button onClick={handleLogout}>로그아웃</button>
        <p style={{ color: "red", marginTop: "10px" }}>오류: {error}</p>
      </div>
    );

  return (
    <div style={{ padding: "20px" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "1px solid #ccc",
          paddingBottom: "10px",
        }}
      >
        <h2>채용 공고 목록 (인증 완료)</h2>
        <div>
          <p style={{ marginRight: "20px", display: "inline-block" }}>
            환영합니다, {currentUser?.email}
          </p>
          <button onClick={handleLogout}>로그아웃</button>
        </div>
      </div>

      {/* 데이터 표시 */}
      <ul>
        {postings.length > 0 ? (
          postings.map((post) => (
            // post.id가 없을 경우를 대비하여 title을 키로 사용
            <li
              key={post.id || post.title}
              style={{
                border: "1px solid #eee",
                padding: "10px",
                margin: "10px 0",
              }}
            >
              <strong>{post.title}</strong> - {post.company_name}
            </li>
          ))
        ) : (
          <p>현재 데이터베이스에 크롤링된 공고가 없습니다.</p>
        )}
      </ul>
    </div>
  );
};

export default PostingsPage;
