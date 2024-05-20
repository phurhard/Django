let currentQuestionIndex = 0;
let questions = [];

document.addEventListener("DOMContentLoaded", function () {
    const categoryItems = document.querySelectorAll('.category-list-item');
    const buttons = document.querySelector('.control');
    const quizContainer = document.getElementById('quiz-container');
    const startQuizButton = document.getElementById('start_quiz');
    const content = document.getElementById('no-quiz-selected-container');

    categoryItems.forEach(function (item) {
        item.addEventListener('click', function () {
            const description = this.getAttribute('data-description');
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

    startQuizButton.addEventListener('click', function () {
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');

        if (selectedCategory) {
            fetch(`http://127.0.0.1:8000/main/quiz/${selectedCategory.value}/`, {
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
                questions = data.question_set;
                displayQuestion(currentQuestionIndex);
                buttons.classList.remove('d-none');
                content.classList.add('d-none');
            })
            .catch(err => {
                console.error('Error occurred: ', err);
            });
        } else {
            console.error("You haven't selected any category");
        }
    });

    window.showNextQuestion = function() {
        if (currentQuestionIndex < questions.length - 1) {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        } else {
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        }
    }

    window.showPreviousQuestion = function() {
        if (currentQuestionIndex > 0) {
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        }
    }

    function displayQuestion(index) {
        quizContainer.innerHTML = ''; // Clear previous question

        if (index >= questions.length) {
            quizContainer.innerHTML = '<p>Quiz completed!</p>';
            buttons.classList.add('d-none');
            return;
        }

        const question = questions[index];
        const questionElement = document.createElement('div');
        questionElement.innerHTML = `<h2>${question.question_text}</h2>`;

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
});
