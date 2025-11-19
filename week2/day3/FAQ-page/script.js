const button = document.querySelector("button");
const main = document.querySelector("main");
button.addEventListener("click", function() {
    main.classList.toggle("expanded");
    button.innerHTML = main.classList.contains("expanded") ? "COLLAPSE FAQS" : "EXPAND FAQS";

});

const questions = document.querySelectorAll(".question");
const answers = document.querySelectorAll(".answer");
const icons = document.querySelectorAll(".question i");

for (let i = 0; i < questions.length; i++) {
  questions[i].addEventListener("click", function () {
    questions[i].classList.toggle("active");
    // icons[i].classList.toggle("fa-circle-chevron-down");
    answers[i].classList.toggle("active");
  });
}