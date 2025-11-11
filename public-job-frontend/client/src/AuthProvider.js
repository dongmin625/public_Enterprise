// public-job-frontend/client/src/AuthProvider.js

import React, { createContext, useContext, useEffect, useState } from 'react';
import { auth } from './firebase'; // <-- 생성한 firebase.js에서 인증 객체를 가져옴
import { onAuthStateChanged } from 'firebase/auth';

// 1. Context 객체 생성
const AuthContext = createContext();

// 2. Context를 쉽게 사용하기 위한 Custom Hook
export const useAuth = () => {
  return useContext(AuthContext);
};

// 3. Provider 컴포넌트: 인증 상태 관리
export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // 컴포넌트 마운트 시 Firebase 인증 상태 변화를 구독
  useEffect(() => {
    // Firebase가 사용자 상태가 바뀔 때마다 호출하는 리스너
    const unsubscribe = onAuthStateChanged(auth, user => {
      setCurrentUser(user);
      setLoading(false); // 로딩 끝
    });

    // 컴포넌트 언마운트 시 구독 해제 (클린업)
    return unsubscribe;
  }, []);

  // Context를 통해 제공할 값
  const value = {
    currentUser, // 현재 로그인된 사용자 정보 (로그아웃 상태면 null)
  };

  // 로딩 중이 아니면 자식 컴포넌트 렌더링
  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};