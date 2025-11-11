// public-job-frontend/client/src/App.js

import React from "react";
import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage"; // 곧 생성할 컴포넌트
import PostingsPage from "./pages/PostingsPage"; // 곧 생성할 컴포넌트
import PrivateRoute from "./PrivateRoute"; // 방금 만든 보호된 경로 컴포넌트

function App() {
  return (
    <div className="App">
      <Routes>
        {/* 로그인 페이지 (인증 없이 접근 가능) */}
        <Route path="/login" element={<LoginPage />} />

        {/* 공고 페이지 (인증 필수 -> PrivateRoute로 보호) */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <PostingsPage />
            </PrivateRoute>
          }
        />

        {/* 다른 경로가 있다면 여기에 추가 */}
      </Routes>
    </div>
  );
}

export default App;
