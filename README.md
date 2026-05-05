# Long Polling Server
Example of long polling.

## Usage
- Start the Docker container: `docker compose up -d --build`. The server will be listening in `http://localhost:8080`
- Stop the Docker container: `docker compose down`

## Endpoints
- `GET /hello`. It returns a welcome message (`Hello from server!`) 
- `GET /poll`. It checks its queue for messages every 200 milliseconds for a period of 20 seconds
- `POST /send`. It receives a message

## Tools
Flask / Python

## Author
ChatGPT 5.2, prompted by Arturo Mora-Rioja.