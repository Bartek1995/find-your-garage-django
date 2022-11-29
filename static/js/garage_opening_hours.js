document.addEventListener("DOMContentLoaded", function () {
checkboxes = document.querySelectorAll('input[type="checkbox"]');

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function () {
    formFieldWrapper = checkbox.closest('.form-field-wrapper');

        inputs = formFieldWrapper.querySelectorAll('input[type="time"]');
        inputs.forEach(input => {
            input.disabled = checkbox.checked;
            if (input.disabled) {
                input.value = null;
            }
        })

        })
    });

});
