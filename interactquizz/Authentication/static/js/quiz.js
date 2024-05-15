document.addEventListener("DOMContentLoaded", function () {
    const categoryItems = document.querySelectorAll('.category-list-item');
    categoryItems.forEach(function (item) {
        // populate it's description to the side menu
        item.addEventListener('click', function () {
            console.log('here');
            const description = this.getAttribute('data-description');
            const content = document.querySelector('content');
            content.textContent = description;
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
});