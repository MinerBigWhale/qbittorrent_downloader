document.addEventListener('DOMContentLoaded', () => {
    const categorySelect = document.getElementById('category');

    // Fetch categories from the backend
    fetch('/api/categories')
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.name;
                option.textContent = category.name;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
        });

    // Handle form submission
    const form = document.getElementById('torrentForm');
    form.addEventListener('submit', event => {
        event.preventDefault();

        const torrentUrl = document.getElementById('torrentUrl').value;
        const category = categorySelect.value;

        fetch('/api/add_torrent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ torrentUrl, category })
        })
            .then(response => response.json())
            .then(data => {
                const responseMessage = document.getElementById('responseMessage');
                responseMessage.textContent = data.message;
            })
            .catch(error => {
                console.error('Error adding torrent:', error);
            });
    });
});