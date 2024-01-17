document.addEventListener("DOMContentLoaded", function(){
    // Once the document is loaded then we can start with the functionalities

    // first we get the values of the categories


    const  url = `http://127.0.0.1:8000/server/`;
    const generate = document.getElementById('generate');
    generate.addEventListener('click', function() {
        // Get the category
        const category = document.getElementById('category');
        const selectedCategory = category.value;
        const spiner = document.querySelectorAll('#generate span')[0];
        spiner.style.display = 'inline-block';
        // console.log(selectedCategory);

        // get the flags

        const flags = document.querySelectorAll('.form-check input[type="checkbox"]:checked');

        const checkedBox = [];

        flags.forEach(function (checkbox) {
            checkedBox.push(checkbox.value);
        });

        // console.log('Flags: ', checkedBox);

        // package the data
        const data = {
            'category': selectedCategory,
            'flags': checkedBox,
        }

        // make a post request to the server

        fetch(url,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data)
        })
        .then(res => res.json())
        .then(data => {
            // console.log(data);
            if (data.error) {
            const message = data.message
            // console.log(message);
            } else {
                const display = document.getElementsByClassName('display')[0];
                spiner.style.display = 'none';
                if (data.data.type === 'twopart') {
                display.innerText = "";
                const setup = document.createElement('p');
                const delivery = document.createElement('p');
                setup.innerText = data.data.setup;
                delivery.innerText = data.data.delivery;
                delivery.style.justifyItems = 'end';

                display.appendChild(setup);
                display.appendChild(delivery);
                // console.log(data.data.delivery);
                // console.log(data.data.setup);

                } else {
                // create a p tag to store the joke inside the display div
                display.innerText = "";
                const paragraph = document.createElement('p');
                paragraph.innerText = data.data.joke;
                display.appendChild(paragraph);
                // console.log(data.data.joke);
                }
            }
        })
        .catch(err => {
            console.log(err);
            alert('Error: ' + err.message);
        });
    });

})