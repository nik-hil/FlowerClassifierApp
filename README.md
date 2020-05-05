# Kaggle data

Trained on dataset https://www.kaggle.com/alxmamaev/flowers-recognition using [Fastai2](https://github.com/fastai/fastai2)



# Docker

Build image
```
docker build -t flower_classifier:latest .
```

Deploy image
```
docker run -d -p 5000:5000 flower_classifier:latest
```

Stop image
```
docker stop 5379b3c3aa9
```

SSH in image
```
docker ps
docker exec -it <Image ID> /bin/bash
```

Remove All image
```
docker system prune -a
```
# Helpful links

 - https://www.fullstackpython.com/blog/develop-flask-web-apps-docker-containers-macos.html
 - https://medium.com/@doedotdev/docker-flask-a-simple-tutorial-bbcb2f4110b5
