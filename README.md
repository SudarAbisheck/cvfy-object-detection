## CVFY Object Detection Demo

This repo contains the code for Object Detection Demo using YOLO Algorithm for [CVFY](https://github.com/Cloud-CV/cvfy-frontend) project.

![img](person.jpg)

## Run the Demo

### with Docker:

```sh
docker run -d --net=host --env CVFY_TOKEN=<PASTE_TOKEN_HERE> sudarabisheck/object-detection
```

### without Docker:

```sh
export CVFY_TOKEN=<PASTE_TOKEN_HERE>
python ./server.py
```

- Replace `<PASTE_TOKEN_HERE>` with the token generated for the demo 
