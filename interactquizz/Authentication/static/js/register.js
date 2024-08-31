// const url = `http://127.0.0.1:8000/`
const url = `https://interactquiz.onrender.com/`
document.addEventListener("DOMContentLoaded", function() {
    // get the toast
    const toastElement = document.getElementById('errorToast');
    const errorToast = new bootstrap.Toast(toastElement, {
        delay: 9000,
        autohide: true
    });
    const registerForm = document.getElementById('registerform');
    const registerButton = registerForm.querySelector('button[type="submit"]');
    const spinner = registerForm.querySelector('.spinner-border');
    const buttonText = registerForm.querySelector('.button-text');
    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        registerButton.disabled = true;
        spinner.classList.remove('d-none');
        buttonText.textContent = 'Creating account...';
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
                return response.json().then(errorData => {
                    data = errorData.data;
                    document.querySelector('#errorToast .toast-body').textContent = errorData.message || 'An error occurred';
                    errorToast.show();
                    registerButton.disabled = false;
                    spinner.classList.add('d-none');
                    buttonText.textContent = 'Register';
                    throw new Error(errorData.message || response.statusText)
                });
            }
            return response.json()
        })
        .then(data => {
            document.querySelector('#errorToast .toast-body').textContent = data.message;
            window.location.href = loginUrl;

        })
        .catch(error => {
            console.log('Error: ', error.message);
            registerButton.disabled = false;
            spinner.classList.add('d-none');
            buttonText.textContent = 'Register';
        });

    })
});