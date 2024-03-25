const API_ENDPOINTS = 'http://127.0.0.1:5003/api/v1/';
//const API_ENDPOINTS = 'https://www.aflahgh.tech/api/';
//const API_ENDPOINTS = 'https://app.aflahgh.tech/api/v1/';

// tokenManager.js
let token = "dXNlckBnbWFpbC5jb206cHdk";
saveToken(token);

 $('.showloader').click(function () {
    Swal.fire(
        'Processing...Please wait!'
    );
    swal.showLoading();
});
// Retrieve the token
let retrievedToken = getToken();

// Function to save the token into Local Storage
function saveToken(token) {
    localStorage.setItem("token", token);
}
console.log("Token Saved!");
// Function to retrieve the token from Local Storage
function getToken() {
    return localStorage.getItem("token");
}

// Function to remove the token from Local Storage
function removeToken() {
    localStorage.removeItem("token");
}

export default API_ENDPOINTS;