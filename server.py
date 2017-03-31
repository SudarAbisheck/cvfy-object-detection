from cvfy import *
from net.build import TFNet
from math import ceil

options = {"model": "cfg/yolo.cfg", "load": "bin/yolo.weights", "threshold": 0.1}

fontFace = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.4
thickness = 1

def _to_color(indx, base):
    """ return (b, g, r) tuple"""
    base2 = base * base
    b = 2 - indx / base2
    g = 2 - (indx % base2) % base
    r = 2 - (indx % base2) / base
    return (b * 127, g * 127, r * 127)

def _classes():
    classes = list()
    file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg/coco.names')
    with open(file, 'r') as f:
        labs = [l.strip() for l in f.readlines()]
        for lab in labs:
            classes.append(lab)                                                                                                                                                                                                                                        
    return classes

classes = _classes()                                                                                                                                                                

def detect(imgfile):
    global classes

    imgcv = cv2.imread(imgfile)
    result = tfnet.return_predict(imgcv)

    for box in result:
        base = int(ceil(pow(len(classes), 1./3)))

        x1,y1,x2,y2 = box['topleft']['x'], box['topleft']['y'], box['bottomright']['x'], box['bottomright']['y']
        conf,label = box['confidence'], box['label']
        
        index = classes.index(label)
        retval,_ = cv2.getTextSize(label, 0, 0.4, 2)
        pad = 4

        cv2.rectangle(imgcv, (x1,y1), (x2,y2), _to_color(index, base), 2)
        cv2.rectangle(imgcv, (x1,y1), (x1+retval[0]+pad, y1+retval[1]+pad), _to_color(index, base), -1)
        cv2.putText(imgcv, label, (x1+pad/2, y1+retval[1]), fontFace, fontScale, (0,0,0), thickness) 

    cv2.imwrite(imgfile, imgcv)
    return imgfile

def log(string):
    sendTextArrayToTerminal(["[INFO] " + string])

@app.route("/event", methods=['POST'])
def event():
    log('Received request')
    images = getImageArray()
    log('Starting Detection using YOLO ... ')
    for image in images:
        detect(image)
    log('Detection Completed')
    sendImageArray(images,'file_path')
    log('Sending Image with detections .... ')
    return jsonify(status='ok')

if __name__ == '__main__':
    token = os.getenv('CVFY_TOKEN')
    if token is not None:
        tfnet = TFNet(options)
        app = register(token)
        app.run()
    else:
        print "\'CVFY_TOKEN\' environment variable not found !!! \n EXITING ...."