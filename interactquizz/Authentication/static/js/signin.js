document.addEventListener("DOMContentLoaded", function() {
    
    document.getElementById('loginform').addEventListener('submit', function(e) {
        e.preventDefault();

        const formdata = new FormData(this);

        const formobject = {}

        for (let [key, value] of formdata.entries()) {
            formobject[key] = value;
        }

        fetch("http://127.0.0.1:8000/auth/login/", {
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
                setTimeout(() => {
                    window.location.href = profileUrl;
                    
                }, 1000
                );
                }

        })
        .catch(error => {
            console.log('Error: ', error);
        });

    })
});