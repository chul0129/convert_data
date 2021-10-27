import os
import json
from xml.etree.ElementTree import  Element,SubElement,ElementTree
from PIL import Image
from jinja2 import PackageLoader, Environment
from xml.sax.saxutils import escape
LabelPath=os.getcwd()+'/labels'

images_dir=os.getcwd()+'/images'
imageFile_list=os.listdir(images_dir)

def indent(elem, level=0):                  #pascal 파일 보기 편하게 공백 넣어주는 함수
    i = "\n" + level*"      "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "       "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
classes=[]
for i in imageFile_list:
    image_name=i
    image_labelPath=LabelPath+"/"+image_name+".json"
    with open(image_labelPath,"r")as f:
        image_json=json.load(f)
    imagePath=images_dir+"/"+image_name
    imageWidth, imageHeight = Image.open(imagePath).size

    width=imageWidth
    height=imageHeight
    #label=image_json['result']['objects'][0]['class']

    root=Element('annotation')
    SubElement(root,'filename').text=image_name+'.json'
    SubElement(root,'path').text=image_labelPath
    source=SubElement(root,'source')
    SubElement(source, 'database').text = 'Unknown'

    size = SubElement(root, 'size')
    SubElement(size, 'width').text = str(width)
    SubElement(size, 'height').text = str(height)
    SubElement(size, 'depth').text = '3'

    SubElement(root, 'segmented').text = '0'
    objectNum=len(image_json['result']['objects'])
    image_name,etc=image_name.split('.')
    for j in range(objectNum):
        obj = SubElement(root, 'object')
        SubElement(obj, 'name').text = image_json['result']['objects'][j]['class']
        classes.append(image_json['result']['objects'][j]['class'])
        SubElement(obj, 'pose').text = 'Unspecified'
        SubElement(obj, 'truncated').text = '0'
        SubElement(obj, 'difficult').text = str(image_json['result']['objects'][j]['difficulty'])

        bndbox=SubElement(obj,'bndbox')
        poly_num=len(image_json['result']['objects'][j]['shape']['polygon'])
        total_x=[]
        total_y=[]
        for p in range(poly_num):
            total_x.append(image_json['result']['objects'][j]['shape']['polygon'][p]['x'])
            total_y.append(image_json['result']['objects'][j]['shape']['polygon'][p]['y'])
        xmin=min(total_x)
        xmax=max(total_x)
        ymin=min(total_y)
        ymax=max(total_y)
        SubElement(bndbox,'xmin').text=str(xmin)
        SubElement(bndbox, 'ymin').text = str(ymin)
        SubElement(bndbox, 'xmax').text = str(xmax)
        SubElement(bndbox, 'ymax').text = str(ymax)
        indent(root)

        tree=ElementTree(root)
        tree.write('./images/'+image_name+'.xml')

classes=set(classes)
classes=list(classes)
#print(classes)

