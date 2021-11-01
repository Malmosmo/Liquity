const DROPDOWN = {
    toggle: "data-dropdown-toggle",
    close: "data-dropdown-close"
}

function InitalizeTailwind() {
    dropdown()
}

// Dropdowns
function dropdown() {
    // toggle
    let elements = document.querySelectorAll("[" + DROPDOWN.toggle + "]")

    for (const element of elements) {
        let targetID = element.getAttribute(DROPDOWN.toggle)
        element.addEventListener("click", () => {
            let target = document.getElementById(targetID)
            target.classList.toggle("hidden")
        })
    }

    // close
    elements = document.querySelectorAll("[" + DROPDOWN.close + "]")

    for (const element of elements) {
        targetID = element.getAttribute(DROPDOWN.close)
        element.addEventListener("click", () => {
            let target = document.getElementById(targetID)
            target.classList.add("hidden");
        })
    }
}


InitalizeTailwind()