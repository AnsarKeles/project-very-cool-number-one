const avatar = document.getElementById("avatar");
const colorPicker = document.getElementById("colorPicker");

colorPicker.addEventListener("input", function () {
    avatar.style.borderColor = colorPicker.value;
});