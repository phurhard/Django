const url = `https://interactquiz.onrender.com/`
document.addEventListener("DOMContentLoaded", function() {
    
    document.getElementById('registerform').addEventListener('submit', function(e) {
        e.preventDefault();

        const formdata = new FormData(this);

        const formobject = {}

        for (let [key, value] of formdata.entries()) {
            formobject[key] = value;
        }

        fetch(`${url}auth/signup/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formobject)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response.json()
        })
        .then(data => {
            window.location.href = loginUrl;

        })
        .catch(error => {
            console.log('Error: ', error);
            alert('An error occurred: ' + error.message);
        });

    })
});