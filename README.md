# Final Project
![Continuous Deployment](https://github.com/software-students-fall2023/5-final-project-rice/actions/workflows/build.yml/badge.svg)
[![app tests](https://github.com/software-students-fall2023/5-final-project-rice/actions/workflows/app-test.yml/badge.svg)](https://github.com/software-students-fall2023/5-final-project-rice/actions/workflows/app-test.yml)

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines. See [instructions](./instructions.md) for details.

## What is Deppops?

Deppops is designed to serve as a medium between people who are interested in trading personal belongings, including clothing, accessories, and other items. Users will be able to post items for others to see and potentially request trades, as well as browse and search for items they would like to trade for. In our app, we have a front end webapp for users that accesses a database through docker containers.(note please do not upload images larger than 16mb as that size is not supported)

## Installation and Usage

### Prerequisites
1. Ensure you have python 3.11 or higher installed 
2. Ensure you have have Docker installed and running on your computer.
3. Optionally, have docker Desktop 

### Github Repository Cloning Option
1. Clone the directory through Git Bash with the command:

```
git clone https://github.com/software-students-fall2023/5-final-project-rice.git
```

2. Open Docker Desktop or a new terminal 

3. In your command prompt/terminal, access the directory where you cloned the repository:
```
cd "path_to_directory"
```

4. From here, run the commands:
```
docker-compose build
docker-compose up
```
5. Now, access the http://127.0.0.1:3000/ in your browser of choice.

6. to end the session 
```
docker-compose stop
```
or 
```
docker-compose down
```

### Website Access Option

With deployment to Digital Ocean, you can access our webapp directly by typing in your url: http://159.203.78.56:3000/

### DockerHub

DockerHub for Continuous Deployment: [rice_db](https://hub.docker.com/r/kingslayerrq/rice_db)[web_app](https://hub.docker.com/r/kingslayerrq/rice)

## Contributors

- [Andrew Huang](https://github.com/andrew0022)
- [Kei Oshima](https://github.com/KeiOshima)
- [Richard Qu](https://github.com/kingslayerrq)
- [Ryan Horng](https://github.com/Ryan-Horng)