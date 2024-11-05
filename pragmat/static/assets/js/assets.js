function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

const existingClickId = getCookie('clickid');
if (existingClickId) {
  const links = document.querySelectorAll('a[href*="/play/"]');
  links.forEach(link => {
    const url = new URL(link.href);
    url.searchParams.set('clickid', existingClickId);
    link.href = url.toString();
  });
}

// Проверка существования формы
const feedbackForm = document.getElementById('feedbackForm');
if (feedbackForm) {
  feedbackForm.addEventListener('submit', function(event) {
    event.preventDefault();
    const responseOutput = document.getElementById('response-output');
    if (responseOutput) {
      responseOutput.classList.remove('d-none');
    }
  });
}

// Проверка существования кнопки
const showTextButton = document.getElementById('showText');
if (showTextButton) {
  showTextButton.addEventListener('click', function () {
    // Get the content div
    var contentDiv = document.querySelector('.content');
    var gradientBlock = document.querySelector('.gradient-block');

    // Проверка существования элементов
    if (contentDiv && gradientBlock) {
      // Check the current height of the content div
      if (contentDiv.style.height === '350px' || contentDiv.style.height === '') {
        // Change height to show all text
        contentDiv.style.height = 'auto'; // Set to auto to show all content
        gradientBlock.classList.remove('d-dark-mode-block'); // Hide the gradient block
        this.textContent = hideTextLabel; // Change button text
        var showMoreArrow = this.querySelector('#showMoreArrow');
        if (showMoreArrow) {
          showMoreArrow.classList.remove('bx-down-arrow-alt'); // Remove down arrow
          showMoreArrow.classList.add('bx-up-arrow-alt'); // Add up arrow
        }
      } else {
        // Reset height to original
        contentDiv.style.height = '350px'; // Reset to original height
        gradientBlock.classList.add('d-dark-mode-block'); // Show the gradient block again
        this.textContent = readMoreLabel; // Change button text back
        var showMoreArrow = this.querySelector('#showMoreArrow');
        if (showMoreArrow) {
          showMoreArrow.classList.remove('bx-up-arrow-alt'); // Remove up arrow
          showMoreArrow.classList.add('bx-down-arrow-alt'); // Add down arrow
        }
      }
    } else {
      console.warn('Content div or gradient block not found.');
    }
  });
} else {
  console.warn('Button with id "showText" not found.');
}


document.addEventListener('DOMContentLoaded', function() {
    const playLinks = document.querySelectorAll('.play-link');
    playLinks.forEach(function(link) {
        link.onclick = function() {
            const url = this.getAttribute('data-href');
            const target = this.getAttribute('data-target');
            window.open(url, target);
        };
    });
});

if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/assets/js/service-worker.js');
    });
}

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    const installButton = document.getElementById('install-link');
    if (installButton) {
        installButton.style.display = 'block';
        installButton.addEventListener('click', (e) => {
            e.preventDefault();
            installButton.style.display = 'none';
            deferredPrompt.prompt();
        });
    }
});

Notification.requestPermission();
