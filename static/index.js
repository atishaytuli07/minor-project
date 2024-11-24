const signInButton = document.getElementById('signIn');
  signInButton.addEventListener('click', () => {
    window.location.href = './login.html';
  });

  const signIn = document.getElementById('signInButton');
  signIn.addEventListener('click', () => {
    window.location.href = './login.html';
  });
  

let accordians = document.getElementsByClassName("FAQ__title");

for (let i = 0; i < accordians.length; i++) {
  accordians[i].addEventListener("click", function () {
    console.log("Accordion clicked");
    let icon = this.querySelector('i');
    console.log("Icon found: ", icon);

    if (icon.classList.contains("fa-plus")) {
      icon.classList.remove("fa-plus");
      icon.classList.add("fa-times");
    } else {
      icon.classList.remove("fa-times");
      icon.classList.add("fa-plus");
    }

    let content = this.nextElementSibling;
    console.log("Content: ", content);

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

