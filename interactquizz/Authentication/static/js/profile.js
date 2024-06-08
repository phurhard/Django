document.addEventListener("DOMContentLoaded", function() {
    // get each elements from the page
    // set image for the user
    const progressBar = document.querySelector('.progress');

    
    fetch('https://source.unsplash.com/random')
    .then(response => {

        document.getElementById("profilePic").src = response.url;
    })
    .catch(error => {
        console.error('Error fetching random image:', error);
    });

    // set the username
    const data = localStorage.getItem('user');
    if (!data) {
        console.log('There is no user data');
    } else {
        const name = JSON.parse(data)
        console.log(JSON.parse(data));
    }

    console.log(progressBar);
})
