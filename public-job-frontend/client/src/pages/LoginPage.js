// public-job-frontend/client/src/pages/LoginPage.js

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { auth } from '../firebase';

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  // 로그인 처리 함수
  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // 오류 초기화

    try {
      // Firebase 로그인 요청
      await signInWithEmailAndPassword(auth, email, password);
      // 로그인 성공 시 '/' 경로(PostingsPage)로 이동
      navigate('/', { replace: true });
    } catch (err) {
      // 로그인 실패 시 오류 메시지 표시
      setError('로그인 실패: ' + err.message);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: 'auto' }}>
      <h1>로그인</h1>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="이메일"
          required
          style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="비밀번호"
          required
          style={{ display: 'block', width: '100%', padding: '10px', marginBottom: '10px' }}
        />
        <button type="submit" style={{ padding: '10px 15px' }}>로그인</button>
      </form>
      {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
    </div>
  );
};

export default LoginPage;