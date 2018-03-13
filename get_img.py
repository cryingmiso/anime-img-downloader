import json
import numpy as np
import cv2
import untangle

maxsize = 512
count = 0

for i in range(10000):
    try:
      import urllib2
      stringreturn = urllib2.urlopen("http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=1girl%20solo&pid="+str(i+3000)).read()
      py3_ver = False
    except ImportError:
      from urllib.request import urlopen
      stringreturn = urlopen("http://safebooru.org/index.php?page=dapi&s=post&q=index&tags=1girl%20solo&pid="+str(i+3000)).read()
      stringreturn = stringreturn.decode('utf-8')
      py3_ver = True

    xmlreturn = untangle.parse(str(stringreturn))
    for post in xmlreturn.posts.post:
        imgurl = "http:" + post["sample_url"]
        print(imgurl)
        if ("png" in imgurl) or ("jpg" in imgurl):
            if not py3_ver:
              resp = urllib2.urlopen(imgurl)
            else:
              resp = urlopen(imgurl)

            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            height, width = image.shape[:2]
            if height > width:
                try:
                    scalefactor = (maxsize*1.0) / width
                    res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                    cropped = res[0:maxsize,0:maxsize]
                except:
                    print("PASS")
                    continue
            if width > height:
                scalefactor = (maxsize*1.0) / height
                res = cv2.resize(image,(int(width * scalefactor), int(height*scalefactor)), interpolation = cv2.INTER_CUBIC)
                center_x = int(round(width*scalefactor*0.5))
                cropped = res[0:maxsize,center_x - int(maxsize/2):center_x + int(maxsize/2)]
            count += 1
            cv2.imwrite("imgs_p3/"+str(count)+".jpg",cropped)

