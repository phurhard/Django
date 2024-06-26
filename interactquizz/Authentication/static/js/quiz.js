let currentQuestionIndex = 0;
let questions = [];
let userAnswers = {};
let quizSubmitted = false;
let checkResultsInterval;
const url = `https://interactquiz.onrender.com/`
// const url = `http://127.0.0.1:8000/`


document.addEventListener("DOMContentLoaded", function () {
    const categoryList = document.getElementById('category-list');
    const categoryItems = document.querySelectorAll('.category-list-item');
    // const buttons = document.querySelector('.control');
    const quizContainer = document.getElementById('quiz-container');
    const startQuizButton = document.getElementById('start_quiz');
    const content = document.getElementById('no-quiz-selected-container');
    const quizSelectedContainer = document.getElementById('quiz-selected-container');
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

    // shuffle function for the question
    function shuffleArray(array) {
        return array.sort(() => Math.random() - 0.5);
    }

    startQuizButton.addEventListener('click', function () {
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');
        const aside = document.querySelector('.aside-column');
        aside.classList.add('d-none');
        
        if (selectedCategory) {
            startQuizButton.disabled = true;
            disableRadioButtons(radioButtons);

            fetch(`${url}main/quiz/${selectedCategory.value}/`, {
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
                // console.log('this is the data', data.level)
                questions = data.quiz.question_set;
                time_limit = data.level.time_limit;
                // pass the time limit in the function for creating a time limit
                const display = document.createElement('div');
                display.classList.add('container');
                quizSelectedContainer.appendChild(display);
                timeInterval(time_limit, display);
                questions = shuffleArray(questions);
                displayQuestion(currentQuestionIndex);
                // buttons.classList.remove('d-none');
                quizSelectedContainer.classList.remove('d-none');
                quizSelectedContainer.classList.add('d-flex');
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

    let timerInterval;
    function timeInterval(time_limit, display) {
        //time limit of quizes
        let time = time_limit * 60;
        let timer = time, minutes, seconds;
        timerInterval = setInterval(function() {
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);

            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;

            display.textContent = minutes + ":" + seconds;

            if (--timer < 0) {
                clearInterval(timerInterval);
                submitQuiz();
            }
        }, 1000);

        // setTimeout(submitQuiz, time * 1000);
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

        const questionTitle = document.createElement('h2');
        questionTitle.classList.add('question-title');
        questionTitle.innerHTML = `<span>${index + 1}. ${question.question_text}</span>`;
        questionElement.appendChild(questionTitle);

        const optionsContainer = document.createElement('div');
        optionsContainer.classList.add('options-container');
        optionsContainer.classList.add('row');
        shuffleArray(question.options);
        question.options.forEach(option => {
            const optionElement = document.createElement('div');
            optionElement.classList.add('option-item');
            optionElement.classList.add('col');
            optionElement.innerHTML = `
                <input type="radio" class="form-check-input" name="option" value="${option.id}" id="option${option.id}">
                <label class="form-check-label" for="options${option.id}">${option.text}</label>
            `;
            optionsContainer.appendChild(optionElement);
        });

        questionElement.appendChild(optionsContainer);
        container.appendChild(questionElement);
        quizContainer.appendChild(container);

        const savedSelection = userAnswers[currentQuestionIndex];
        if (savedSelection !== undefined) {
            document.getElementById(`option${savedSelection}`).checked = true;
        }
        
    };
    // submit the quizzes
    // function submitQuiz() {
    //     clearInterval(timerInterval);
    //     saveSelection();
    //     // console.log('user answers: ', userAnswers);
    //     const Okiki = collateResults();
    //     checkResultsInterval = setInterval(() => {
    //         if (Okiki) {
    //             clearInterval(checkResultsInterval);
    //             console.log('modal should show now');
    //             showModal();
    //         }
    //         console.log('Not here');
    //         console.log(Okiki);
    //     }, 5000);
    // }

    async function submitQuiz() {
        clearInterval(timerInterval);
        saveSelection();

        const resultsProcessed = await collateResults();
        if (resultsProcessed) {
            showModal();
        } else {
            console.error('Results processing failed');
        }
    }
    submitQuizButton.addEventListener('click', function () {
        // alert("You have submitted your quiz, please wait a little bit for your results");
        submitQuiz();

    });

    function getCsrfToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }
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
    // function collateResults() {
    //     const finalAnswers = collectUserAnswers();
    //     const csrftoken = getCsrfToken();
    //     const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');
    //     fetch(`${url}main/submit_quiz/`, {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': csrftoken,
    //             'Authorization': `Bearer ${localStorage.getItem('token')}`
    //         },
    //         body: JSON.stringify(finalAnswers)
    //     })
    //     .then(response => {
    //         if (!response.ok) {
    //             throw new Error('Network response was not ok ' + response.statusText);
    //         }
    //         return response.json();
    //     })
    //     .then(data => {
    //         console.log('finalAnswers: ', finalAnswers);
    //         console.log('Success:', data);
    //         fetch(`${url}main/results/${selectedCategory.value}`, {
    //         method: 'GET',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Authorization': `Bearer ${localStorage.getItem('token')}`
    //         }
    //         })
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok ' +    response.statusText);
    //             }
    //             return response.json();
    //         })
    //         .then(data => {
    //             console.log('Success:', data);
    //             return true;
    //         })
    //         .catch(error => {
    //             console.error('Error: ', error);
    //         });
    //     })
    //     .catch(error => {
    //         console.error('Error: ', error);
    //     });

    // }

    async function collateResults() {
        const finalAnswers = collectUserAnswers();
        const csrftoken = getCsrfToken();
        const selectedCategory = document.querySelector('input[name="quiz_type"]:checked');

        try {
            const response = await fetch(`${url}main/submit_quiz/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',

                    'X-CSRFToken': csrftoken,
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify(finalAnswers)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }

            const resultsResponse = await fetch(`${url}main/results/${selectedCategory.value}`, {
                method: 'GET',
                'headers': {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });

            if (!resultsResponse.ok) {
                throw new Error('Network reponse was not ok ' + resultsResponse.statusText);
            }

            const resultsData = await resultsResponse.json();
            console.log('success: ', resultsData);
            return true;
        } catch (error) {
            console.error('Error: ', error);
            return false;
        }
    }

});
