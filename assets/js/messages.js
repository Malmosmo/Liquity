// Toast Buttons
let toastCloseBtns = document.getElementsByClassName("toast-close")

for (const closeBtn of toastCloseBtns) {
    closeBtn.addEventListener("click", () => {
        let target = closeBtn.getAttribute("target")
        document.getElementById(target).classList.toggle("show")
    })
}

// Toasts
let toasts = document.getElementsByClassName("toast")
for (const toast of toasts) {
    setTimeout(() => {
        toast.classList.toggle("show")
    }, 5000)
}
