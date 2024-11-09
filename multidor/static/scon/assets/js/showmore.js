
document.getElementById('showText').addEventListener('click', function() {
    // Get the content div
    var contentDiv = document.querySelector('.content');
    var gradientBlock = document.querySelector('.gradient-block');

    // Check the current height of the content div
    if (contentDiv.style.height === '350px' || contentDiv.style.height === '') {
        // Change height to show all text
        contentDiv.style.height = 'auto'; // Set to auto to show all content
        gradientBlock.style.display = 'none'; // Hide the gradient block
        this.textContent = 'Скрыть текст'; // Change button text
        this.querySelector('#showMoreArrow').classList.remove('bx-down-arrow-alt'); // Remove down arrow
        this.querySelector('#showMoreArrow').classList.add('bx-up-arrow-alt'); // Add up arrow
    } else {
        // Reset height to original
        contentDiv.style.height = '350px'; // Reset to original height
        gradientBlock.style.display = 'block'; // Show the gradient block again
        this.textContent = 'Читать полностью'; // Change button text back
        this.querySelector('#showMoreArrow').classList.remove('bx-up-arrow-alt'); // Remove up arrow
        this.querySelector('#showMoreArrow').classList.add('bx-down-arrow-alt'); // Add down arrow
    }
});

