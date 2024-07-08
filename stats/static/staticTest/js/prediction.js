function loading() {
    const season = document.getElementById('season').value;
    const loadingDiv = document.getElementById('loading');
    const form = document.getElementById('seasonForm');

    loadingDiv.classList.remove('hidden');
    form.classList.add('hidden');

    setTimeout(() => {
        window.location.href = `prediction.html?season=${season}`;
    }, 2000); // 2 seconds delay for suspense

    return false; // Prevent form submission
}