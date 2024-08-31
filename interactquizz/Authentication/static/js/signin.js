// const url = 'http://127.0.0.1:8000'
const url = `https://interactquiz.onrender.com/`
document.addEventListener("DOMContentLoaded", function() {
    // get the csrf cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue
    }
    const csrftoken = getCookie('csrftoken');
    // get the toast
    const toastElement = document.getElementById('errorToast');
    const errorToast = new bootstrap.Toast(toastElement, {
        delay: 9000,
        autohide: true
    });
    const successToastElement = document.getElementById('successToast');
    const successToast = new bootstrap.Toast(successToastElement, {
        delay: 5000,
        autohide: true
    });

    const loginForm = document.getElementById('loginform');
    const loginButton = loginForm.querySelector('button[type="submit"]');
    const spinner = loginButton.querySelector('.spinner-border');
    const buttonText = loginButton.querySelector('.button-text');

    async function handleLoginSuccess(data) {
        try {
            // Store tokens and user data asynchronously
            await localStorage.setItem('token', data.access);
            await localStorage.setItem('refresh', data.refresh);
            const user = JSON.stringify(data.data);
            await localStorage.setItem('user', user);
    
            // Re-enable the login button and hide the spinner
            loginButton.disabled = false;
            spinner.classList.add('d-none');
            buttonText.textContent = 'Login';
    
            // Show success toast
            document.querySelector('#successToast .toast-body').textContent = data.message || 'Login successful';
            successToast.show();
    
            // Fetch the profile asynchronously
            const response = await fetch(profileUrl, {
                method: "GET",
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`,
                    'Content-Type': 'application/json'
                },
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            // Redirect to profile page
            window.location.href = profileUrl;
        } catch (error) {
            console.error('An error occurred: ', error);
            loginButton.disabled = false;
            spinner.classList.add('d-none');
            buttonText.textContent = 'Login';
    
        }
    }

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        // disable the login button to prevent resubmission,  show spinner and change text
        loginButton.disabled = true;
        spinner.classList.remove('d-none');
        buttonText.textContent = 'Processing...';


        const formdata = new FormData(this);

        const formobject = {}

        for (let [key, value] of formdata.entries()) {
            formobject[key] = value;
        }

        fetch(loginUrl, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify(formobject),
            credentials: 'same-origin'
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    document.querySelector('#errorToast .toast-body').textContent = errorData.message || 'An error occurred';
                    errorToast.show();
                    loginButton.disabled = false;
                    spinner.classList.add('d-none');
                    buttonText.textContent = 'Login';
                    throw new Error(errorData.message || response.statusText)
                });
                
            }
            return response.json();
        })
        .then(data => {
            if (data.success !== true) {
                loginButton.disabled = false;
                spinner.classList.add('d-none');
                buttonText.textContent = 'Login';

            } else {
                handleLoginSuccess(data);
            }
        })
        .catch(error => {
            console.log('Error occured: ', error.message);
            loginButton.disabled = false;
            spinner.classList.add('d-none');
            buttonText.textContent = 'Login';
        });

    })
});