// public-job-frontend/client/src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import { BrowserRouter } from 'react-router-dom'; // 라우터 임포트
import { AuthProvider } from './AuthProvider'; // AuthProvider 임포트
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/* BrowserRouter로 앱 전체를 감싸서 라우팅 활성화 */}
    <BrowserRouter>
      {/* AuthProvider로 앱 전체를 감싸서 인증 상태 전역 제공 */}
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);

reportWebVitals();
