/**
 * Navbar
 */
let icon = document.getElementById("nav-icon");
icon.addEventListener("click", () => {
    icon.classList.toggle("bi-list");
    icon.classList.toggle("bi-x");
});

/**
 * Messages
 */
// Toast Buttons
let toastCloseBtns = document.getElementsByClassName("toast-close")

for (const closeBtn of toastCloseBtns) {
    closeBtn.addEventListener("click", () => {
        let targetID = closeBtn.getAttribute("target")
        let target = document.getElementById(targetID)
        target.classList.toggle("show")
        target.classList.toggle("d-none")
    })
}

// Toasts
let toasts = document.getElementsByClassName("toast")
for (const toast of toasts) {
    setTimeout(() => {
        toast.classList.toggle("show")
    }, 5000)
}

/**
 * Drinks
 */
// Time update on cards
let cardAdds = document.getElementsByClassName("drink-add")
for (const cardAdd of cardAdds) {
    cardAdd.addEventListener("click", () => {
        let date = new Date().toLocaleTimeString().slice(0, -3);
        let targetID = cardAdd.getAttribute("target")
        document.getElementById(targetID).value = date

    })
}