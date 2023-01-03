
const buttons = document.querySelectorAll('#modal-open-button');

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const accordion = button.closest('.accordion-item');

        const accordionButton = accordion.querySelector('.accordion-button');
        const accordionContent = accordion.querySelector('.accordion-collapse')
        accordionContent.classList.add('d-block');

        const modalFade = accordion.querySelector('.fade');

        modalFade.addEventListener('click',() => {
            accordionContent.classList.remove('d-block');
            accordionButton.classList.add('collapsed');
            document.body.classList.remove('modal-open');
            if (document.querySelector('.modal-backdrop'))
                document.querySelector('.modal-backdrop').remove();
            modalFade.classList.remove('show');
            modalFade.style.display = 'none';
            document.body.removeAttribute('style');
        })
    });
});