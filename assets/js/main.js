function init() {
    initSearch();
    initGroup();
}

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

// Message FadeOut
function setTimer(delay, target) {
    let fade;

    // Fade out
    let func1 = () => {
        let element = document.getElementById(target);
        if (!element.style.opacity) {
            element.style.opacity = 1;
        }

        if (element.style.opacity > 0) {
            element.style.opacity -= 0.025;
        } else {
            clearInterval(fade);

            document.getElementById("messages").style.display = "none";
        }
    };

    // For delay
    let func2 = () => {
        fade = setInterval(func1, 1);
    };

    setTimeout(func2, delay);
}
