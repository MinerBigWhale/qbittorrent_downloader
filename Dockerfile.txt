FROM python:3.9-slim

# Install dependencies
RUN pip install flask requests

# Copy addon files
COPY qbittorrent_api.py /app/qbittorrent_api.py
COPY web_ui /app/web_ui
COPY run.sh /app/run.sh

# Set working directory
WORKDIR /app

# Expose the Flask web server port
EXPOSE 5000

# Run the addon
CMD ["bash", "run.sh"]