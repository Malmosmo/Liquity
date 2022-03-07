let darkMode = localStorage.getItem("dark-mode")
const darkModeToggle = document.querySelector("#dark-mode-toggle")

const enableDarkMode = () => {
    document.body.classList.add("dark-mode")

    localStorage.setItem("dark-mode", "on")
}

const disableDarkMode = () => {
    document.body.classList.remove("dark-mode")

    localStorage.setItem("dark-mode", "off")
}

if (darkMode === "on") {
    enableDarkMode()
}

const toggleDarkMode = () => {
    darkMode = localStorage.getItem("dark-mode")

    if (darkMode === "on") {
        disableDarkMode()
    } else {
        enableDarkMode()
    }
}

darkModeToggle.addEventListener("click", () => { toggleDarkMode() })
