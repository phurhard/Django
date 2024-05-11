document.addEventListener("DOMContentLoaded", function() {
    
    document.getElementById('loginform').addEventListener('submit', function(e) {
        e.preventDefault();

        const formdata = new FormData(this);

        const formobject = {}

        for (let [key, value] of formdata.entries()) {
            formobject[key] = value;
        }
        console.log(formobject);

        fetch("http://127.0.0.1:8000/auth/login/", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formobject)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('An error occured in accessing the backend');

            }
            return response.json();
        })
        .then(data => {
            if (data.success !== true) {
                alert("Credentials are not correct")
            } else {
                localStorage.setItem('token', data.access);
                localStorage.setItem('refresh', data.refresh);
                localStorage.setItem('user', data.user);
                setTimeout(() => {
                    window.location.href = "profile.html";
                }, 5000
                );
                }

        })
        .catch(error => {
            console.log('Error: ', error);
        });

    })
});