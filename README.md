# A-Shared-Mileage-Diary
A distributed journal where each user can use their node to mark their mileage, and the car used. The system would calculate the individual costs and the amount of money owed by each driver.

## Seting up the system


Running this project should be a fairly simple task because all the modules are already encapsulated into their own docker containers.

First either clone the repository or download it to your local machine:

```console
$ git clone https://github.com/Tarekreda/A-Shared-Mileage-Diary.git

$ cd A-Shared-Mileage-Diary/
```

once you are inside the directory of the project move into the kafka-docker folder to start the kafka docker container 

```console
$ cd kafka-docker
```

run the following command in your terminal to start the container, and wait for 10 secs to make sure the topics and the service is already running.  you should be good to go once you start seeing the logs from kafka and zookeeper.

```console
$ docker compose up
```
Notice: if you run an older version of docker compose you might want to use the command "docker-compose" instead. 

leave the current folder and move into the flask-redis folder, and start the service container as well.

```console
$ cd flask-redis 
$ docker compose up
```

The flask app container should be up and running now, you can check it on : http://127.0.0.1:5000/

for the sake of simplicity and demonstration, we are setting up the app with two user and two cars, choose the user and the car and enter the mileage,you can then move to http://127.0.0.1:5000/getcalculation to check all the diary log, you can also check the bill calculations on http://127.0.0.1:5000/bill





## Extended functionality and testing the system:


to demonstrate the proper functionality of the kafka-docker, you can go to the app node folder and run the command 


```console
$ cd app-node
$ pip install -r requirements.txt
$ flask run -h localhost -p 3000
```

the app should be up and running on : http://127.0.0.1:3000/

you can send other diary entries from this node and check that they are updated at the same time on the other docker node, which was demonstrated in the demo video : https://drive.google.com/file/d/1uSqDDStytTZCF2jOJyDYZclu8qMpFcRA/view?usp=sharing


once you are done, you can shut down every container using the command 


```console
$ docker compose stop
```

The code of the project is the product of our work. However some minor snippets, configurations, and inspiration was drawn from the references linked below:

* for setting up the kafka docker:

https://towardsdatascience.com/kafka-docker-python-408baf0e1088
https://www.baeldung.com/kafka-docker-connection
https://stackoverflow.com/questions/56576014/docker-kafka-connect-two-different-containers

* for setting up the flask app:

https://medium.com/geekculture/streaming-model-inference-using-flask-and-kafka-3476d9ff5ca5
https://realpython.com/intro-to-python-threading/

* for setting up flask-redis docker:
https://collabnix.com/dockerize-an-api-based-flask-app-and-redis-using-docker-desktop/



 
