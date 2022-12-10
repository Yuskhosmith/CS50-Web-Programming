# Tests...

## Unittest Methods
- assertEqual
- assertNotEqual
- assertTrue
- assertFalse
- assertIn
- assertNotIn

# CI/CD
Continous Integration and Continous Delivery

- Continuous Integration
    - Frequent merges to main branch
    - Automated unit testin
- Continuous Delivery
    - Short release schedules

## Github Actions
Uses YAML, YAML is a file format that structures its data in terms of key value pair like JSON object or Python dictionary

```yaml
    key1: value1
    key2: value2
    key3: 
        -item1
        -item2
        -item3
```

Test the deployed code `.github/workflows/ci.yml`
```yaml
# .github/workflows/ci.yml or .yaml
name: Testing
on: push

jobs:
    test_project:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v2
        - name: Run Django unit tests
            run: |
                pip3 install --user django
                python3 manage.py test
```

### Explanation
`name: Testing`: name

`on: push`: when should the workflow run, on push...

`jobs:`: what tasks should happen when the workflow runs

`test_project:`: job name(can be anything you want)

`runs-on: ubuntu-latest`: what machine should the job run on, github has its own `vm` for various `os`

`steps:` what actions should happen

`- uses: actions/checkout@v2`: checkout from the branch it was pushed to

`- name: Run Django unit tests` just for understanding purposes, a name for what's about to run (beneath)

`run:` literally run

`pip3 install --user django` install django on the vm, if there are other requirements you should install them as well

`python3 manage.py test` run thethingy


## Docker
Instead of creating a virtual machine which will create different virtual operating systems for different tests....this takes alot of memory. Docker on the other hand, are light weight, they don't run differnt OS but they run on the host OS.... Containerization.

```Dockerfile
# docker image to base the instructions below, here we're saying, use python3
FROM python:3

# copy the current directory into /usr/src/app (the container)
COPY . /usr/src/app

# change the working directory to the container
WORKDIR /usr/src/app

# install the requirements into the container
RUN pip install -r requirements.txt

# the command to be run as a comma separated list/array
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```

Docker also allows us to run two differnt things side by side, for examplet the code above runs the application, but let's say we're using postgresql for our database, we'll need to create another container for us to run our postgres database.

Docker Compose allows us to to the above but allow both containers to communicate.
```yml
version: '3'

# each service is a container
services:
    db:
        image: postgres
    
    web:
        build: .
        volumes:
            - .:/usr/src/app
        ports:
            - "8000:8000"
```

To start-up these services, we'll run

```cmd
docker-compose up
```

To see the containers that are currently running:

```terminal
docker ps
```

To run a normal command on the docker container, you'll get the container id and run the ffg:

```powershell
docker exec -it <containerid> bash -l
```

then you can start using normal django commands like createsuperuser, migrate etc. Then ctrl + D to logout.