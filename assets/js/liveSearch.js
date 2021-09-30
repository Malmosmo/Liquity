let beerDictionary = {};

function initSearch() {
    // create dictionary from cards
    let elements = document.getElementsByClassName("CARD_SEARCH");

    for (let i = 0; i < elements.length; i++) {
        let item = elements[i];
        let name = item.firstElementChild.lastElementChild.firstElementChild.firstElementChild.innerHTML
            .trim()
            .toLowerCase();

        beerDictionary[name] = item;
    }
}

function search() {
    let element = document.getElementById("liveSearch");

    let noChanges = Object.keys(beerDictionary).length;

    for (const [key, value] of Object.entries(beerDictionary)) {
        if (!key.includes(element.value.toLowerCase())) {
            value.style.display = "none";
            noChanges -= 1;
        } else {
            value.style.display = "block";
        }
    }

    // Text displayed when there is no result
    let el = document.getElementById("BEER_LIST");

    if (noChanges === 0) {
        el.style.display = "block";
    } else {
        el.style.display = "none";
    }
}

/**
 * Profile Search
 */

function profileSearch() {
    let element = document.getElementById("profileName");
    if (element.value.length < 1) { return; };
    let params = "?name=" + element.value;

    let callback = (args) => {
        let ul = document.getElementById("LIST");
        ul.innerHTML = "<li class='list-group-item active' aria-current='true'>Profiles</li>";

        for (const profile of args.profiles) {
            let li = document.createElement('li');
            li.classList.add('list-group-item');

            let div1 = document.createElement('div');
            div1.classList.add('d-flex');
            div1.classList.add('px-1');
            div1.classList.add('py-1');

            let div2 = document.createElement('div');
            div2.classList.add('friend-image');
            div2.classList.add('rounded-circle');
            div2.style.backgroundImage = "url(" + profile.image + ")";

            let div3 = document.createElement('div');
            div3.classList.add('vertical-center');
            div3.classList.add('flex-grow-1');

            let span = document.createElement('span');
            span.classList.add('ms-2');

            let a = document.createElement('a');
            a.classList.add('link')
            a.classList.add('text-dark')
            a.innerHTML += profile.name
            a.href = "/profile/" + profile.pk + "/"


            span.appendChild(a);
            div3.appendChild(span);
            div1.appendChild(div2);
            div1.appendChild(div3);
            li.appendChild(div1);
            ul.appendChild(li);
        }
    };

    ProfileApiCall(params, callback)
}

function ProfileApiCall(params, callback) {
    const userAction = async () => {
        const response = await fetch("/api/profile/" + params);
        const myJson = await response.json();

        if (myJson.status === "Error") {
            throw "Invalid API call";
        } else {
            callback(myJson);
        }
    };

    userAction();
}