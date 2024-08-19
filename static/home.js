document.addEventListener('DOMContentLoaded', () => {
    // Supposons que l'URL de la photo de profil soit stockée dans le localStorage
    const profilePicUrl = localStorage.getItem('profilePicUrl');

    if (profilePicUrl) {
        const imgBanner = document.getElementById('profile-pic-banner-img');
        imgBanner.src = profilePicUrl;
        imgBanner.style.display = 'block';
    }
});