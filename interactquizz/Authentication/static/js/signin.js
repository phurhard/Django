const url = `https://interactquiz.onrender.com/`
document.addEventListener("DOMContentLoaded", function() {
    
    document.getElementById('loginform').addEventListener('submit', function(e) {
        e.preventDefault();

        const formdata = new FormData(this);

        const formobject = {}

        for (let [key, value] of formdata.entries()) {
            formobject[key] = value;
        }

        fetch(`${url}auth/login/`, {
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
            return response.json();
        })
        .then(data => {
            if (data.success !== true) {
                alert(data.message);
            } else {
                localStorage.setItem('token', data.access);
                localStorage.setItem('refresh', data.refresh);
                const user = JSON.stringify(data.data);
                localStorage.setItem('user', user);
                fetch(profileUrl, {
                    method: "GET",
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`,
                        'Content-Type': 'application/json'
                    },
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response;
                })
                .then(data => {
                    window.location.href = '/auth/profile'
                })
                .catch(error => {
                    console.error('An error occured ', error);
                });
            }
        })
        .catch(error => {
            console.log('Error: ', error);
        });

    })
});