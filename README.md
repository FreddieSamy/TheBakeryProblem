# TheBakeryProblem

## Installation
### remote docker image
You can simply pull a docker image and run it
```
docker pull freddiesamy/the-bakery-problem
```
```
docker run -p 5000:5000 -d freddiesamy/the-bakery-problem
```

### local docker image

1. clone this repo
```
git clone git@github.com:FreddieSamy/TheBakeryProblem.git
```

2. navigate to the repo folder
```
cd TheBakeryProblem/
```

3. build the docker image
```
docker build --tag the-bakery-problem .
```

4. run the container
```
docker run -d -p 5000:5000 --name the-bakery-problem  the-bakery-problem
```

### without dockers
1. clone this repo
```
git clone git@github.com:FreddieSamy/TheBakeryProblem.git
```

2. navigate to the repo folder
```
cd TheBakeryProblem/
```

3. install requirements
```
pip install -r requirements.txt
```

4. start the server
```
python3 app.py
```


Finally, browse to localhost port 5000 : 
http://localhost:5000/
