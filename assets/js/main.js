function apiGroupCall(params, callback) {
    const userAction = async () => {
        const response = await fetch("/api/group/" + params);
        const myJson = await response.json();

        if (myJson.status === "Error") {
            throw "Invalid API call";
        } else {
            callback(myJson);
        }
    };

    userAction();
}

function apiSingleCall(params, callback) {
    const userAction = async () => {
        const response = await fetch("/api/single/" + params);
        const myJson = await response.json();

        if (myJson.status === "Error") {
            throw "Invalid API call";
        } else {
            callback(myJson);
        }
    };

    userAction();
}

// Time update on Beer cards
function updateTime(pk) {
    // Pad time with zeros
    function pad(arg) {
        return (arg < 10 ? "0" : "") + arg;
    }

    let element = document.getElementById("time_" + pk.toString());
    let date = new Date();

    element.value = pad(date.getHours()) + ":" + pad(date.getMinutes());
}