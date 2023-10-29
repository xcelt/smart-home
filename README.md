# Smart Home Prototype (SSA 2023)
Prototype for The Smart Home by The A Team (Group 1), as part of the Secure Systems Architecture module.

## Setup
### Prerequisites
* Docker version: ^24.0.6

### Installing
#### For Windows
1. Make sure the docker is started. On Windows - this can be done by starting the Docker Desktop app.
1. In the smart-home (root) directory, run `docker-compose up -d --build`
#### For Linux
1. `cd smart-home-dev-clean`
2. `sudo apt install docker`
3.  `sudo systemctl start docker` (sys-auto) or ` sudo dockerd` (manual)
4.  `docker-compose up -d --build
5.  Once finished, on browser type `localhost:3000` for frontend and `localhost:8000/api/decices/` for backend

## Testing
Once the docker containers are running, the following sections contain guided instructions for testing the frontend and backend, respectively. 
### Frontend
1. To view real-time logs while the app is running, run `docker logs -f frontend_service`
1. Open a browser and navigate to <i>localhost:3000</i>

### Backend
1. To view real-time logs whie testing the api, run `docker logs -f backend_service`
1. Open a browser and navigate to <i>localhost:8000/api</i> 

# References
* 
