# TheBakeryProblem

## How To Run
You can simply pull a docker image and run it
```
$ docker pull freddiesamy/the-bakery-problem
```
```
$ docker run -p 5000:5000 -d freddiesamy/the-bakery-problem
```

OR

1. clone this repo
```
$ git clone git@github.com:FreddieSamy/TheBakeryProblem.git
```

2. navigate to the repo folder
```
$ cd TheBakeryProblem/
```

3. build the docker image
```
$ docker build -tag the-bakery-problem .
```

4. run the container
```
$ docker run -p 5000:5000 -d the-bakery-problem
```

5. Finally, browse to localhost port 5000 : 
http://localhost:5000/
