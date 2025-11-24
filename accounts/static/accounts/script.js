document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  form.addEventListener("submit", function(event) {
    event.preventDefault(); // stop page reload

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    console.log("Form submitted!");
    console.log("Username:", username);
    console.log("Password:", password);
  });
});