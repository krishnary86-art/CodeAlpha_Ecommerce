document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });

    const qtyInputs = document.querySelectorAll('.cart-item-qty input[type="number"]');
    qtyInputs.forEach(function (input) {
        input.addEventListener('change', function () {
            const min = parseInt(input.min, 10) || 1;
            const max = parseInt(input.max, 10) || 999;
            let val = parseInt(input.value, 10);
            if (isNaN(val) || val < min) input.value = min;
            if (val > max) input.value = max;
        });
    });
});
