
    document.querySelectorAll('.promo-code-button').forEach(function (promoButton) {

        promoButton.addEventListener('click', function () {
            // Копируем текст
            const textToCopy = promoButton.querySelector('.promo-code-text-button').textContent;
            const textarea = document.createElement('textarea');
            textarea.value = textToCopy;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);

            const promoLabel = promoButton.querySelector('.promo-label');
            promoLabel.textContent = "Скопирован";
            setTimeout(function () {
                promoLabel.textContent = "Промокод";
            }, 2000);
        });

        promoButton.addEventListener('mouseenter', function () {
            promoButton.querySelector('.promo-label').textContent = "Копировать";
        });

        promoButton.addEventListener('mouseleave', function () {
            promoButton.querySelector('.promo-label').textContent = "Промокод";
        });
    });

