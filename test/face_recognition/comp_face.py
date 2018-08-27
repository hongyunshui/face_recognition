#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/7/18 10:40 PM
# @Author  : hys
# @Site    : 
# @File    : comp_face.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com

import face_recognition
# 读取图片信息
jobs_image = face_recognition.load_image_file("image/pics_i_know/hong.jpg")
obama_image = face_recognition.load_image_file("image/pics_unknow/hg.jpg")
unknown_image = face_recognition.load_image_file("image/aaa.jpg")
# 获得图片encoding
jobs_encoding = face_recognition.face_encodings(jobs_image)[0]
obama_encoding = face_recognition.face_encodings(obama_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
# 匹配图片encoding
results = face_recognition.compare_faces([jobs_encoding, obama_encoding], unknown_encoding)
print("***")
print(results)
print("***")
labels = ['jobs', 'obama']

print('results:'+str(results))

for i in range(0, len(results)):
    if results[i] == True:
        print('The person is:'+labels[i])

