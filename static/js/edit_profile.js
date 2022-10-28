
document.addEventListener('DOMContentLoaded', function() {
    const cleanImageCheckbox = document.querySelector('#id_clean_profile_image');
    const profileImageBox = document.querySelector('#avatar_select');
    const profileImageInput = document.querySelector('#id_avatar');

    cleanImageCheckbox.addEventListener('change', function() {
        profileImageBox.classList.toggle('d-none');
        profileImageInput.value = null;
    });
});
