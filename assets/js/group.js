let GROUP_ADD = [];

// Group - Add Event Listeners
function initGroup() {
    let elements = document.getElementsByClassName("GROUP_ADD");

    for (const element of elements) {
        let id = element.getAttribute("id");

        element.addEventListener("click", () => {
            groupAdd(id.replace("group_add_", ""));
        });
    }

    let element = document.getElementById("groupSubmit");
    let pk = element.getAttribute("group-pk");
    element.addEventListener("click", () => {
        groupAddSubmit(pk);
    });
}

// Group - add pks to list
function groupAdd(pk) {
    let element = document.getElementById("group_add_" + pk);
    let status = element.getAttribute("add-status");

    if (status == "on") {
        GROUP_ADD.push(pk);

        element.setAttribute("add-status", "off");
        element.innerHTML = "Remove";

        element.classList.add("text-danger");
        element.classList.remove("text-success");
    } else {
        const index = GROUP_ADD.indexOf(pk);
        GROUP_ADD.splice(index, 1);

        element.setAttribute("add-status", "on");
        element.innerHTML = "Add to group";

        element.classList.add("text-success");
        element.classList.remove("text-danger");
    }
}

// Group - submit list
function groupAddSubmit(pk) {
    if (GROUP_ADD.length > 0) {
        window.location.href = GROUP_URL + pk + "/?add=" + GROUP_ADD.join("-");
    } else {
        window.location.href = GROUP_URL + pk;
    }
}
