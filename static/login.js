
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-analytics.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";


const firebaseConfig = {
  apiKey: "AIzaSyCQorx3AlSCmJTNFqg0-XzJh5o3W0dmFtc",
  authDomain: "netflixconversaai.firebaseapp.com",
  projectId: "netflixconversaai",
  storageBucket: "netflixconversaai.appspot.com",
  messagingSenderId: "1003525164231",
  appId: "1:1003525164231:web:7c8c14f420912cadc8c2e2",
  measurementId: "G-YLVSW707J8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);


const submit = document.getElementById('submit');
submit.addEventListener("click", function (event) {
  event.preventDefault()
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      // Signed up 
      const user = userCredential.user;
      alert("Logged' In....")
      window.location.href = "page2.html";
      // ...
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      alert("errorMessage")
      // ..
    });
})

const auth = getAuth(app);

