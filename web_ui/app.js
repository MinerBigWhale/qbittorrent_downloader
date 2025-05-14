document.addEventListener('DOMContentLoaded', () => {
    const categorySelect = document.getElementById('category');
    const dropZone = document.getElementById('dropZone');
    const torrentFileInput = document.getElementById('torrentFile');

    // Fetch categories from the backend
    fetch('../api/categories')
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categorySelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error('Error fetching categories:', error);
        });

    // Highlight drop zone on drag over
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.style.backgroundColor = '#e9e9e9';
    });

    // Remove highlight on drag leave
    dropZone.addEventListener('dragleave', () => {
        dropZone.style.backgroundColor = '#f9f9f9';
    });

    // Handle file drop
    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.style.backgroundColor = '#f9f9f9';

        const files = event.dataTransfer.files;
        if (files.length > 0) {
            torrentFileInput.files = files; // Assign the dropped file to the input
            const fileName = files[0].name; // Get the file name
            dropZone.querySelector('p').textContent = `Selected file: ${fileName}`; // Display the file name
        }
    });

    // Handle click on drop zone
    dropZone.addEventListener('click', () => {
        torrentFileInput.click(); // Trigger the file input click
    });

    // Update file name when selected via file input
    torrentFileInput.addEventListener('change', () => {
        if (torrentFileInput.files.length > 0) {
            const fileName = torrentFileInput.files[0].name;
            dropZone.querySelector('p').textContent = `Selected file: ${fileName}`; // Display the file name
        }
    });

    // Handle form submission
    const form = document.getElementById('torrentForm');
    form.addEventListener('submit', event => {
        event.preventDefault();

        const torrentFile = torrentFileInput.files[0];
        const category = categorySelect.value;

        if (!torrentFile) {
            alert('Please select a .torrent file.');
            return;
        }

        const formData = new FormData();
        formData.append('torrentFile', torrentFile);
        formData.append('category', category);

        fetch('../api/add_torrent', {
            method: 'POST',
            body: formData
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
                    progressBar.setAttribute('data-progress', Math.round(torrent.progress * 100)); // Set percentage value

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

    // Automatically update the torrent list every 5 seconds
    setInterval(fetchActiveTorrents, 5000);
});