FROM python:2.7-onbuild 
RUN ["/bin/bash", "-c", "set -o pipefail && wget -O - https://www.dropbox.com/s/186l87idtwks5di/yolo.weights?dl=1 > bin/yolo.weights"]
CMD ["python", "./server.py"]