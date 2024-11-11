document.addEventListener('DOMContentLoaded', function() {
    const playLinks = document.querySelectorAll('.hl');
    playLinks.forEach(function(link) {
        link.onclick = function() {
            const url = this.getAttribute('data-href');
            const target = this.getAttribute('data-target');
            window.open(url, target);
        };
    });
});