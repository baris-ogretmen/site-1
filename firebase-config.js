// Firebase yapılandırması (Kendi bilgilerini buraya yapıştır)
const firebaseConfig = {
  apiKey: "AIzaSy...", 
  authDomain: "projen-adi.firebaseapp.com",
  projectId: "projen-adi",
  storageBucket: "projen-adi.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abcdef"
};

// Firebase'i başlat
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}
