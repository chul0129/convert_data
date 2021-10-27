import json
import os

MetaPath="C:/Users/yk291/PycharmProjects/jsonlabeling/meta/seouldata"
LabelPath="C:/Users/yk291/PycharmProjects/jsonlabeling/labels"
file_list=os.listdir(MetaPath)
json_list=[]
for i in file_list:
    with open(MetaPath+"/"+i,"r")as line:
        json_list.append(json.load(line))

#for i in range(len(json_list)):
#with open('C:\\test.json', 'w', encoding='utf-8') as make_file:
    #json.dump(json_data, make_file, indent="\t")
for i in range(len(json_list)):
    label_path = LabelPath+"/"+json_list[i]['label_id']+'.json'
    file_name= json_list[i]['data_key']
    os.rename(label_path, LabelPath+'/'+file_name+'.json')
    json_list[i]['label_id']=file_name
    json_list[i]['label_path'] ="labels/"+file_name+".json"
    with open(MetaPath+'/'+json_list[i]['data_key']+'.json','w',encoding='utf-8') as make_file:
        json.dump(json_list[i],make_file,indent="\t")
#print(json_list[0])
#a=str(json_list[0]['label_path'])
#file_name,ext=a.split('.')
#print(file_name)
#for i in json_list:
 #   dict.append([json_list[i]['data_key'],json_list[i]['label_id']])
#dict_list[0]['data_key'])
#dict_list[0]['label_id'])
