# MGolf - Backend

## Description
This project is a backend service for `MGolf application`. 
It's built using the FastAPI framework in Python.

## Project Structure

```
.
├── ...
├── constant/
├── database/
│   ├── models/
│   ├── query/
│   ├── ...
│   └── database.py
├── env/
├── middleware/
├── routers/
│   ├── __init__.py
│   └── ...
├── schemas/
│   ├── __init__.py
│   └── ...
├── templates/
├── utils/
├── .env
├── .gitignore
├── cspsell.json
├── main.py
├── README.md
└── requirements.txt
```
- `constant`: define constants for the project
- `database`: database config and operations. 
- `database/query`: SQL query for the database (store procedures,...)
- `database/models`: class model orm for the database
- `env`: contains environment-related files.
- `middleware`: hanle the middleware functions (token, write log)
- `schemas`: request, response models.
- `routers`: contains all routing in the application.
- `templates`: contains excel template for report and import
- `utils`: utility modules that are used across the project.
- .env: store environment variables related to SSO - Keycloak
- .gitignore
- main.py: entry point of our application.
- README.md: this file
- requirements.txt: lists the Python dependencies that need to be installed for the project.

## Installation
Follow these steps to install and run the project:
1. Clone the project from its repository:
```bash
git clone https://gitlab.com/product.mbf2/mgolf_backend.git
```
2. Navigate into the project directory:
```bash
cd mgolf_backend
```
3. Create virtual environment
```bash
python -m venv env
```

4. Active virtual environment
```bash
env/Scripts/activate
```

5. Install the required Python packages.
```bash
pip install -r requirements.txt
```

6. Run the FastAPI server:
```bash
uvicorn main:app --reload
```
## Deployment on CentOS 7 server
- Typical startup steps
1. If you want to start or stop the program: Run the script `start.sh` or `stop.sh`
2. In case of a faulty git commit, please run the `rollback.sh` script to revert to the previous error-free git commit.
3. In case the program needs to disconnect from the Database, adjust the value of the `CONNECT_DB` variable in the `config.properties` file to `Off`, and vice versa to enable the connection, set it to `On`.

## Deployment with Docker
1. Push image into registry local MBF via:
- Step 1: Login into registry local (***user/password on Trello***)
```bash
docker login 10.39.125.26:8000
```
- Step2: Add this line to Docker's daemon.json file and restart the Docker Daemon:
(C:\ProgramData\Docker\config\daemon.json on windows, /etc/docker/daemon.json on linux)
```bash
{ 
    "insecure-registries":["10.39.125.26:8000"]
}
```
```bash
sudo systemctl restart docker
```
- Step 3: run command:
```bash
./push_image.sh
```
- Step 4: check image push successful: 10.39.125.26:80
3. On server copy file docker-compose.yml and folder file_logs (first time setup)
- Step 1: Login into registry local (***user/password on Trello***)
```bash
docker login 10.39.125.26:8000
```
- Step 2: On docker-compose file, change environmental variables as needed: (***.env file get on Trello***)
    + CONNECT_DB: ON/OFF (Toggle Log Database)
    + SQLALCHEMY_DATABASE_URL: postgresql://{username}:{pass}@{hostname}:{port}/{database_name} (Connection Chain to Postgresql Database)
4. On server run command:
```bash
docker-compose pull --ignore-pull-failures && docker-compose up -d
```
5. Stop container
```bash
docker-compose down
```
6. Logs
```bash
docker-compose logs -f --tail=100 api-gateway
```
7. SSH
```bash
docker exec -it api-gateway bash
```
8. ON/OFF DATABASE
- Step 1: Change CONNECT_DB=OFF on .env file
- Step 2: Run command
```bash
docker compose down && docker compose up -d
```
## Authors
- Nguyễn Đức Đạt - Email: dat.nguyenduc@mobifone.vn
- Lê Tất Can - Email: can.lt@mobifone.vn