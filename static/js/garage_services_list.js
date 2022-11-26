const mechanicalRepairCheckbox = document.querySelector('#id_mechanical_repairs');
const inputs = document.querySelectorAll("input[type='checkbox']");

inputs.forEach(checkbox => {
    let inputParent = checkbox.parentElement;
    
    if (checkbox.checked) {
        inputParent.classList.add('card-selected');
    }

    inputParent.addEventListener('click', function() {
        inputParent.classList.toggle('card-selected');
        checkbox.checked = !checkbox.checked;
    });
});
