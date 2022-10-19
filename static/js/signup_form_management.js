function addDisabledToButtons(buttons){
    buttons.forEach(button => {
        button.setAttribute('disabled', '');
    })}

function removeDisabledFromButtons(buttons){
    buttons.forEach(button => {
        button.removeAttribute('disabled');
    })}

function changeTextOfButtons(buttons, text){
    buttons.forEach(button => {
        button.innerHTML = text;
    })}

function addClassToButtons(buttons, className){
    buttons.forEach(button => {
        button.classList.add(className);
    })}
    
function removeClassfromButtons(buttons, className){
    buttons.forEach(button => {
        button.classList.remove(className);
    })}

document.addEventListener('DOMContentLoaded', function(){
    const customerButtons = document.querySelectorAll('#customer_button_0, #customer_button_1');
    const entrepreneurButtons = document.querySelectorAll('#entrepreneur_button_0, #entrepreneur_button_1');
    const signupButton = document.querySelector('#signup_button')
    const customerSelectCheckbox = document.querySelector('#id_usertype_0');
    const entrepreneurSelectCheckbox = document.querySelector('#id_usertype_1');
    
    if (customerSelectCheckbox.checked)
    {
        addDisabledToButtons(customerButtons);
        changeTextOfButtons(customerButtons, 'Wybrano');
        addClassToButtons(customerButtons, 'buttons__btn--selected');
        signupButton.removeAttribute('disabled');
    }
    else if (entrepreneurSelectCheckbox.checked)
    {
        addDisabledToButtons(entrepreneurButtons);
        changeTextOfButtons(entrepreneurButtons, 'Wybrano');
        addClassToButtons(entrepreneurButtons, 'buttons__btn--selected');
        signupButton.removeAttribute('disabled');
    }

    customerButtons.forEach(button => {
        button.addEventListener('click', function(){
        signupButton.removeAttribute('disabled');

        customerSelectCheckbox.checked = true;
        entrepreneurSelectCheckbox.checked = false;

        addDisabledToButtons(customerButtons);
        addClassToButtons(customerButtons, 'buttons__btn--selected');
        removeClassfromButtons(entrepreneurButtons, 'buttons__btn--selected');
        changeTextOfButtons(customerButtons, 'Wybrano');
        removeDisabledFromButtons(entrepreneurButtons);
        changeTextOfButtons(entrepreneurButtons, 'Wybierz');
    });
});
    entrepreneurButtons.forEach(button => {
        button.addEventListener('click', function(){
        signupButton.removeAttribute('disabled');

        entrepreneurSelectCheckbox.checked = true;
        customerSelectCheckbox.checked = false;

        addDisabledToButtons(entrepreneurButtons);
        addClassToButtons(entrepreneurButtons, 'buttons__btn--selected');
        removeClassfromButtons(customerButtons, 'buttons__btn--selected');
        changeTextOfButtons(entrepreneurButtons, 'Wybrano');
        removeDisabledFromButtons(customerButtons);
        changeTextOfButtons(customerButtons, 'Wybierz');
    });
});

})