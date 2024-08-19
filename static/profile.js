document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('profile-form');
    const fileInput = document.getElementById('profile-pic');
    const imgPreview = document.getElementById('profile-pic-img');

    // Afficher un aperçu de l'image sélectionnée
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imgPreview.src = e.target.result;
                imgPreview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

    // Envoyer le formulaire pour sauvegarder la photo (à compléter avec un backend)
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        // Envoyer le formulaire à votre serveur via fetch ou XMLHttpRequest
        fetch('/upload-profile-pic', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Photo de profil mise à jour avec succès !');
                // Vous pouvez également mettre à jour la photo dans la bannière ici
            } else {
                alert('Erreur lors de la mise à jour de la photo de profil.');
            }
        });
    });
});
