document.addEventListener('DOMContentLoaded', function(){
    const navHref = document.querySelectorAll('.nav-link')
    const navMark = document.querySelector('#navbarNavAltMarkup')

    navHref.forEach(element => element.addEventListener('click', () =>
        navMark.classList.remove('show')
    ))

})


