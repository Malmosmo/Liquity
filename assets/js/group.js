// group add init
let newMembers = [];
let friends = document.getElementsByClassName("lq-group-add")

for (const friend of friends) {
    friend.addEventListener("click", () => {
        let status = friend.getAttribute("add-status");
        const profile = friend.getAttribute("profile")

        // toggle color
        friend.classList.toggle("text-danger");
        friend.classList.toggle("text-success");

        if (status == "on") {
            newMembers.push(profile);

            friend.setAttribute("add-status", "off");
            friend.innerHTML = "Remove";
        } else {
            const index = newMembers.indexOf(profile);
            newMembers.splice(index, 1);

            friend.setAttribute("add-status", "on");
            friend.innerHTML = "Add";
        }
    })
}

// group add submit
if (document.getElementById("groupSubmit") != null) {
    let submitBtn = document.getElementById("groupSubmit")
    submitBtn.addEventListener("click", () => {
        let url = submitBtn.getAttribute("url")

        if (newMembers.length > 0) {
            window.location.href = url + "?add=" + newMembers.join("-");
        } else {
            window.location.href = url;
        }
    })
}
