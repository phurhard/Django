document.addEventListener("DOMContentLoaded", function () {
    const categoryItems = document.querySelectorAll('.category-list-item');
    categoryItems.forEach(function (item) {
        // populate it's description to the side menu
        item.addEventListener('click', function () {
            console.log('here');
            const description = this.getAttribute('data-description');
            const content = document.getElementById('content');
            if (content) {
                content.textContent = description;
            } else {
                console.log('Unable to find the element with the id Content');
            }
        });
        item.addEventListener('mouseover', function () {
            const description = this.getAttribute('data-description');
            const tooltip = document.createElement('div');
            tooltip.classList.add('category-description');
            tooltip.style.display = 'block';
            tooltip.textContent = description;
            this.appendChild(tooltip);
        });
        item.addEventListener('mouseout', function () {
            const tooltip = this.querySelector('.category-description');
            if (tooltip) {
                tooltip.remove();
            }
        });

    });

    // collect the selected category and send to the backend for updating the page

    const start_quiz = document.getElementById('start_quiz');
    start_quiz.addEventListener('click', function() {
        const selected_category = document.querySelector('input:checked');
        if (selected_category) {
            console.log(selected_category.id);
            // make a fetch to the server for the questions
            fetch(`http://127.0.0.1:8000/main/quiz/${selected_category.id}/`, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem('token')}`,
                    "Content-Type": "application/json"
                },
            })
            .then(res => {
                if (!res.ok) {
                    throw new Error(res.statusText);
                }
                return res.json();
            })
            .then(data => {
                console.log(data);
            })
            .catch(err => {
                console.error('error occured: ', err);
            });


        } else {
            console.error("You haven't selected any category");
        }

    })

});