let currentQuestionIndex = 0;
let questions = [];

document.addEventListener("DOMContentLoaded", function () {
    const categoryItems = document.querySelectorAll('.category-list-item');
    const buttons = document.querySelectorAll('.controls');

    categoryItems.forEach(function (item) {
        // populate it's description to the side menu
        item.addEventListener('click', function () {
            const description = this.getAttribute('data-description');
            const content = document.getElementById('content');
            if (content) {
                content.textContent = description;
            } else {
                console.error('Unable to find the element with the id Content');
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
            console.log('buttons: ', buttons);

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
                questions = data.question_set;
                displayQuestion(currentQuestionIndex);
            })
            .catch(err => {
                console.error('Error occured: ', err);
            });


        } else {
            console.error("You haven't selected any category");
        }

    });
});
    //update the display with questions


function displayQuestion(index) {
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = ''; // Clear previous question

    if (index >= questions.length) {
        quizContainer.innerHTML = '<p>Quiz completed!</p>';
        return;
    }

    const question = questions[index];
    const questionElement = document.createElement('div');
    questionElement.innerHTML = `<h2>${question.text}</h2>`;
    
    question.options.forEach(option => {
        const optionElement = document.createElement('div');
        optionElement.innerHTML = `
            <input type="radio" name="option" value="${option.id}">
            <label>${option.text}</label>
        `;
        questionElement.appendChild(optionElement);
    });


    quizContainer.appendChild(questionElement);
}

function showNextQuestion() {
    currentQuestionIndex++;
    displayQuestion(currentQuestionIndex);
}

function showpreviousQuestion() {
    currentQuestionIndex--;
    displayQuestion(currentQuestionIndex);
}
