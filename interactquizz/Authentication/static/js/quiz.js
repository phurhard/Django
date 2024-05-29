let currentQuestionIndex = 0;
let questions = [];
let userAnswers = {};

document.addEventListener("DOMContentLoaded", function () {
    const categoryList = document.getElementById('category-list');
    const categoryItems = document.querySelectorAll('.category-list-item');
    const buttons = document.querySelector('.control');
    const quizContainer = document.getElementById('quiz-container');
    const startQuizButton = document.getElementById('start_quiz');
    const content = document.getElementById('no-quiz-selected-container');
    const submitQuizButton = document.getElementById('submit-quiz');
    const radioButtons = categoryList.querySelectorAll('input[type="radio"]');

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

    function disableRadioButtons(radioButtons) {
        radioButtons.forEach(radio => {
            radio.disabled = true;
        });
    }  

    startQuizButton.addEventListener('click', function () {
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');
        const aside = document.querySelector('.aside-column');
        aside.classList.add('d-none');
        
        if (selectedCategory) {
            startQuizButton.disabled = true;
            disableRadioButtons(radioButtons);

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
            saveSelection();
            currentQuestionIndex++;
            displayQuestion(currentQuestionIndex);
        } else {
            saveSelection();
            displayQuestion(currentQuestionIndex);
        }
    }

    window.showPreviousQuestion = function() {
        if (currentQuestionIndex > 0) {
            saveSelection();
            currentQuestionIndex--;
            displayQuestion(currentQuestionIndex);
        }
    }

    window.redirect = function() {
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');
        window.location.href = `/main/corrections/${selectedCategory.value}/`
    }

    function displayQuestion(index) {
        quizContainer.innerHTML = ''; // Clear previous question

        if (index >= questions.length) {
            quizContainer.innerHTML = '<p class="">Quiz completed!</p>';
            // buttons.classList.add('d-none');
            return;
        }
        const container = document.createElement('div');
        container.classList.add('card')
        const question = questions[index];

        const questionElement = document.createElement('div');
        questionElement.classList.add('card-body');

        const questionTitle = document.createElement('div');
        questionTitle.classList.add('question-title');
        questionTitle.innerHTML = `<h2>${index + 1}. ${question.question_text}</h2>`;
        questionElement.appendChild(questionTitle);

        const optionsContainer = document.createElement('div');
        optionsContainer.classList.add('options-container');
        question.options.forEach(option => {
            const optionElement = document.createElement('div');
            optionElement.classList.add('option-item');
            optionElement.innerHTML = `
                <input type="radio" class="form-check-input" name="option" value="${option.id}" id="option${option.id}">
                <label class="form-check-label" for="options${option.id}">${option.text}</label>
            `;
            optionsContainer.appendChild(optionElement);
        });

        questionElement.appendChild(optionsContainer);
        quizContainer.appendChild(questionElement);

        const savedSelection = userAnswers[currentQuestionIndex];
        if (savedSelection !== undefined) {
            document.getElementById(`option${savedSelection}`).checked = true;
        }
        
    };
    // submit the quizzes
    // const correctionURL = "{% url 'view-corrections' %}";
    submitQuizButton.addEventListener('click', function () {
        saveSelection();
        console.log('user answers: ', userAnswers);
        collateResults();
        showModal();

    });

   
    function showModal() {
        const dynamicModal = new bootstrap.Modal(document.getElementById('dynamicModal'), {
            backdrop: 'static',
            keyboard: false
        });
        dynamicModal.show();

        document.getElementById('dynamicModal').addEventListener('hidden.bs.modal', function () {
            document.getElementById('dynamicModal').remove();
        });
    }

    // save the answers of the questions to userAnswers so the answers can be persisted 
    function saveSelection() {
        const selectedOption = document.querySelector('input[name="option"]:checked');
        if (selectedOption) {
            userAnswers[currentQuestionIndex] =  selectedOption.value;
        }
    }

    function collectUserAnswers() {
        const answers = {};
        Object.keys(userAnswers).forEach(index => {
            const question = questions[index];
            answers[question.id] = userAnswers[index];
        });
        return answers;
    }

    // collate the results
    function collateResults() {
        const finalAnswers = collectUserAnswers();
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');
        fetch('http://127.0.0.1:8000/main/score/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(finalAnswers)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('finalAnswers: ', finalAnswers);
            console.log('Success:', data);
            fetch(`http://127.0.0.1:8000/main/results/${selectedCategory.value}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' +    response.statusText);
                }
                return response.json();
            })
            .then(data => {
                console.log('Success:', data);
            })
            .catch(error => {
                console.error('Error: ', error);
            });
        })
        .catch(error => {
            console.error('Error: ', error);
        });

    }
});
