document.addEventListener('DOMContentLoaded', () => {
    const categorySelect = document.getElementById('category');

    // Fetch categories from the backend
    fetch('../api/categories')
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

        fetch('../api/add_torrent', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ torrentUrl, category })
        })
            .then(response => response.json())
            .then(data => {
                const responseMessage = document.getElementById('responseMessage');
                responseMessage.textContent = data.message;
                fetchActiveTorrents(); // Refresh active torrents after adding a new one
            })
            .catch(error => {
                console.error('Error adding torrent:', error);
            });
    });

    // Fetch and display active torrents
    function fetchActiveTorrents() {
        fetch('../api/active_torrents')
            .then(response => response.json())
            .then(torrents => {
                const activeTorrentsContainer = document.querySelector('.torrent-table');
                activeTorrentsContainer.innerHTML = ''; // Clear previous list

                torrents.forEach(torrent => {
                    const torrentRow = document.createElement('div');
                    torrentRow.className = 'torrent-row';

                    const name = document.createElement('div');
                    name.className = 'torrent-name';
                    name.textContent = torrent.name;

                    const progressContainer = document.createElement('div');
                    progressContainer.className = 'torrent-progress-container';

                    const progressBar = document.createElement('div');
                    progressBar.className = 'torrent-progress-bar';
                    progressBar.style.width = `${torrent.progress * 100}%`;

                    progressContainer.appendChild(progressBar);

                    const status = document.createElement('div');
                    status.className = 'torrent-status';
                    status.textContent = torrent.state;

                    torrentRow.appendChild(name);
                    torrentRow.appendChild(progressContainer);
                    torrentRow.appendChild(status);

                    activeTorrentsContainer.appendChild(torrentRow);
                });
            })
            .catch(error => {
                console.error('Error fetching active torrents:', error);
            });
    }

    // Initial fetch of active torrents
    fetchActiveTorrents();
});