// Profiles
if (document.getElementById('profileSearchInput') != null) {
    let searchInput = document.getElementById("profileSearchInput")
    let url = searchInput.getAttribute("api-url")

    let inputValue = ""

    searchInput.addEventListener("keyup", debounce(() => {

        // prevents API call on shift, ctrl, etc.
        let newInput = searchInput.value.trim()

        if (newInput.length >= 1 && inputValue != newInput) {
            inputValue = newInput

            // API call
            fetch(url + "?name=" + inputValue).then(response => {
                return response.json()
            }).then(json => {
                let searchList = document.getElementById("profileSearchList")
                let child = searchList.firstElementChild

                // list header
                searchList.innerHTML = ""
                searchList.appendChild(child)

                // result number
                let results = document.getElementById("results")
                results.innerHTML = json.profiles.length

                // result list
                for (const profile of json.profiles) {
                    let li = document.createElement("li")
                    li.setAttribute("class", "list-group-item d-flex align-items-center")

                    let img = document.createElement("img")
                    img.setAttribute("width", "40")
                    img.setAttribute("height", "40")
                    img.setAttribute("class", "image rounded-circle")
                    img.setAttribute("src", profile.image)

                    let link = document.createElement("a")
                    link.setAttribute("href", "/profile/" + profile.pk + "/")
                    link.setAttribute("class", "link text-dark ms-2")
                    link.appendChild(document.createTextNode(profile.name));

                    li.appendChild(img)
                    li.appendChild(link)
                    searchList.appendChild(li)
                }
            })
        }
    }, 250));
}

// Drinks
if (document.getElementById('drinkInput') != null) {
    let drinkInput = document.getElementById('drinkInput')

    // init
    let cards = document.getElementsByClassName("lq-card")
    let drinks = []

    for (const card of cards) {
        let name = card.getAttribute("name")

        drinks.push({
            "domElement": card,
            "name": name
        })
    }

    // Event listener
    drinkInput.addEventListener("keyup", () => {
        let inputValue = drinkInput.value.trim()
        for (const drink of drinks) {
            if (!drink.name.includes(inputValue)) {
                drink.domElement.setAttribute("hidden", "")
            } else {
                drink.domElement.removeAttribute("hidden")
            }
        }
    })
}