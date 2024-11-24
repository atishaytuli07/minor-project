import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-analytics.js";
import { getAuth, createUserWithEmailAndPassword, sendEmailVerification, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCQorx3AlSCmJTNFqg0-XzJh5o3W0dmFtc",
  authDomain: "netflixconversaai.firebaseapp.com",
  projectId: "netflixconversaai",
  storageBucket: "netflixconversaai.appspot.com",
  messagingSenderId: "1003525164231",
  appId: "1:1003525164231:web:7c8c14f420912cadc8c2e2",
  measurementId: "G-YLVSW707J8"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

const submitButton = document.querySelector('.button-submit');
const signupSubmit = document.getElementById("signupSubmit"); // Add this for sign-up link handling

// Event listener for the login button
submitButton.addEventListener("click", function (event) {
  event.preventDefault();

  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const isSignup = signupSubmit.innerText === "Sign Up"; // Check if the user is in sign-up mode

  if (isSignup) {
    // Sign-up flow
    createUserWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        const user = userCredential.user;
        sendEmailVerification(user)
          .then(() => {
            alert("Account created !! Enjoy Recommendations !!");
            window.location.href = "page2.html"; // Redirect to another page or stay here as needed
          })
          .catch((error) => {
            const errorMessage = error.message;
            alert("Error sending verification email: " + errorMessage);
          });
      })
      .catch((error) => {
        const errorMessage = error.message;
        alert("Error creating account: " + errorMessage);
      });
  } else {
    // Login flow
    signInWithEmailAndPassword(auth, email, password)
      .then((userCredential) => {
        // Successfully signed in
        alert("Successfully logged in! enjoy Netflix !");
        window.location.href = "page2.html"; // Redirect to your dashboard or home page
      })
      .catch((error) => {
        const errorMessage = error.message;
        alert("Error signing in");
      });
  }
});

// Handle the "Sign Up" / "Log In" switch
signupSubmit.addEventListener("click", function () {
  const isCurrentlySignup = signupSubmit.innerText === "Sign Up";
  signupSubmit.innerText = isCurrentlySignup ? "Log In" : "Sign In"; // Toggle the text
  submitButton.innerText = isCurrentlySignup ? "Create Account" : "Sign Up"; // Toggle button text
});
