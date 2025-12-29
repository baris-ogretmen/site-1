const firebaseConfig = {
  apiKey: "AIzaSyAqeO-yQyQPnLsOqKmSNvVH23WPvneIjaU",
  authDomain: "shaped-totem-481514-c5.firebaseapp.com",
  projectId: "shaped-totem-481514-c5",
  storageBucket: "shaped-totem-481514-c5.firebasestorage.app",
  messagingSenderId: "519295049418",
  appId: "1:519295049418:web:7d04e18c4ea36bc088de33",
  measurementId: "G-10ENZQDXX1"
};

// BU KISIM ÇOK ÖNEMLİ, MUTLAKA EKLE:
if (!firebase.apps.length) {
    firebase.initializeApp(firebaseConfig);
}
