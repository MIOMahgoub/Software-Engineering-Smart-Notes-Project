document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const globalError = document.getElementById("error");

  form.addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username");
    const password = document.getElementById("password");
    const confirm = document.getElementById("confirm");

    const usernameError = document.getElementById("username-error");
    const passwordError = document.getElementById("password-error");
    const confirmError = document.getElementById("confirm-error");

    // Reset previous errors
    [username, password, confirm].forEach(input => input.classList.remove("error"));
    [usernameError, passwordError, confirmError].forEach(span => span.textContent = "");
    globalError.textContent = "";

    let hasError = false;

    if (!username.value.trim()) {
      username.classList.add("error");
      usernameError.textContent = "Username is required.";
      hasError = true;
    } else if (username.value.trim().toLowerCase() === "takenuser") {
      // Example check for "already taken"
      username.classList.add("error");
      usernameError.textContent = "This username is already taken.";
      hasError = true;
    }

    if (!password.value) {
      password.classList.add("error");
      passwordError.textContent = "Password is required.";
      hasError = true;
    }

    if (password.value !== confirm.value) {
      confirm.classList.add("error");
      confirmError.textContent = "Passwords do not match.";
      hasError = true;
    }

    if (hasError) {
      globalError.textContent = "Please fix the errors above before submitting.";
      return;
    }

    console.log("Form submitted!");
    console.log("Username:", username.value);
    console.log("Password:", password.value);
  });
});
