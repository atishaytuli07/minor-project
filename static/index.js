document.getElementById("signInButton").addEventListener("click", function () {
  window.location.href = "login.html";
});

let accordian = document.getElementsByClassName("FAQ__title");

for (let i = 0; i < accordian.length; i++) {
  accordian[i].addEventListener("click", function () {
    if (this.childNodes[1].classList.contains("fa-plus")) {
      this.childNodes[1].classList.remove("fa-plus");
      this.childNodes[1].classList.add("fa-times");
    } else {
      this.childNodes[1].classList.remove("fa-times");
      this.childNodes[1].classList.add("fa-plus");
    }

    let content = this.nextElementSibling;
    if (content.style.maxHeight) {
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}

function toggleSignInForm() {
  const signInButton = document.getElementById("signInButton");
  const buttonText = signInButton.querySelector(".text");

  if (buttonText.textContent === "Sign In") {
    buttonText.textContent = "Sign Up";
    signInButton.setAttribute("onclick", "signUp()");
  } else {
    buttonText.textContent = "Sign In";
    signInButton.setAttribute("onclick", "signIn()");
  }
}



function signUp() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Redirect to page2.html upon successful sign up
      window.location.href = "page2.html";
    })
    .catch((error) => {
      // Handle errors here
      const errorCode = error.code;
      const errorMessage = error.message;
      console.error(errorCode + " - " + errorMessage);
    });
}

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.11.1/firebase-analytics.js";

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