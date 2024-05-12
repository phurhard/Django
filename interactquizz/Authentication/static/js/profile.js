document.addEventListener("DOMContentLoaded", function() {
    // get each elements from the page
    // set image for the user
    
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
        const name = JSON.parse(data).username
        document.getElementsByName('username')[0].value = name;
    }

    // get the answers from the server
    
})
