const hamburger = document.getElementsByClassName("ham")[0];
const nav = document.getElementsByTagName("nav")[0];

hamburger.addEventListener("click", () => {
    nav.classList.toggle("active");
    hamburger.innerHTML = hamburger.innerHTML === "N" ? "X" : "N";
});
