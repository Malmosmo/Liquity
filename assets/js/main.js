// function apiGroupCall(params, callback) {
//     const userAction = async () => {
//         const response = await fetch("/api/group/" + params);
//         const myJson = await response.json();

//         if (myJson.status === "Error") {
//             throw "Invalid API call";
//         } else {
//             callback(myJson);
//         }
//     };

//     userAction();
// }

// function apiSingleCall(params, callback) {
//     const userAction = async () => {
//         const response = await fetch("/api/single/" + params);
//         const myJson = await response.json();

//         if (myJson.status === "Error") {
//             throw "Invalid API call";
//         } else {
//             callback(myJson);
//         }
//     };

//     userAction();
// }
