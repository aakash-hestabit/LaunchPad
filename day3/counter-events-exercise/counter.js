const increaseBtn = document.getElementById("increase-btn");
const decreaseBtn = document.getElementById("decrease-btn");
const display = document.getElementsByTagName("span")[0];
let counter = 0;

increaseBtn.addEventListener("mouseenter", () => {
    counter++;
    display.innerHTML = counter;
});

decreaseBtn.addEventListener("mouseenter", () => {
    counter--;
    display.innerHTML = counter;
});