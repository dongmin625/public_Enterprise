// public-job-frontend/client/src/firebase.js

import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// 🚨 당신의 최종 firebaseConfig 정보 (클라이언트용)
const firebaseConfig = {
    apiKey: "AIzaSyDDsRrZmEd-i8XjInS1uU2ums0U3dKJoz4", 
    authDomain: "publicenterprise-e6284.firebaseapp.com",
    projectId: "publicenterprise-e6284",
    storageBucket: "publicenterprise-e6284.firebasestorage.app",
    messagingSenderId: "1060350791473",
    appId: "1:1060350791473:web:f5793e13ba0bc40b20ea10",
    measurementId: "G-7E39XJFXFH",
};

// Firebase 앱 초기화
const app = initializeApp(firebaseConfig);

// Firebase 인증 객체 내보내기
export const auth = getAuth(app);