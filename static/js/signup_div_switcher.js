document.addEventListener('DOMContentLoaded', function(){
    const customerButtons = document.querySelectorAll('#customer_button')
    const entrepreneurButtons = document.querySelectorAll('#entrepreneur_button')

    const accountTypeNormalDiv = document.querySelector('#select-account-type-normal')
    const accountTypeCarouselDiv = document.querySelector('#select-account-type-carousel')
    const signupBox = document.querySelector('#signup-box')

    customerButtons.forEach(button => {
        button.addEventListener('click', function(){
            switchDivAfterBtnClick()
            const isCustomerFormRadioCheck = document.querySelector('#id_usertype_0')
            isCustomerFormRadioCheck.checked = true
        })
    });
    entrepreneurButtons.forEach(button => {
        button.addEventListener('click', function(){
            switchDivAfterBtnClick()
            const isEntrepreneurFormRadioCheck = document.querySelector('#id_usertype_1')
            isEntrepreneurFormRadioCheck.checked = true
        })
    });

    function switchDivAfterBtnClick(){
                accountTypeNormalDiv.classList.add('visuallyHidden')
                accountTypeCarouselDiv.classList.add('visuallyHidden')

                setTimeout(function () {
                    accountTypeNormalDiv.classList.add('hidden');
                    accountTypeCarouselDiv.classList.add('hidden')
                    signupBox.classList.remove('d-none')
                }, 300);

                setTimeout(function () {
                    signupBox.classList.remove('visuallyHidden')
                }, 1000);
            }}
)


