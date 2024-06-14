document.addEventListener("DOMContentLoaded", function() {
    // get each elements from the page
    // set image for the user
    const progressBar = document.querySelector('.progress');

    // set the username
    const data = localStorage.getItem('user');
    if (!data) {
        // console.log('There is no user data');
    } else {
        // const name = JSON.parse(data)
        // console.log(JSON.parse(data));
    }

    // console.log(progressBar);
})
