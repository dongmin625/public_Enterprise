// public-job-frontend/client/src/PrivateRoute.js

import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthProvider'; // 인증 상태를 가져오는 훅

// 인증된 사용자만 접근할 수 있도록 보호하는 컴포넌트
const PrivateRoute = ({ children }) => {
  const { currentUser } = useAuth(); // 현재 사용자 정보

  // 사용자가 로그인되어 있으면 자식 컴포넌트(children)를 렌더링
  // 로그인되어 있지 않으면 '/login' 경로로 리다이렉트
  return currentUser ? children : <Navigate to="/login" replace />;
};

export default PrivateRoute;