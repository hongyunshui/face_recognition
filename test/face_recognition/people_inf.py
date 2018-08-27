#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 8/20/18 10:24 AM
# @Author  : hys
# @Site    : 
# @File    : people_inf.py
# @Software: PyCharm
# @Desc....:
# @license.:.Copyright(C), Your Company
# Contact : george.zw513@gamil.com
from video_capture import VideoCapture
import numpy as np


class People:
    """人"""
    def __init__(self):
        """初始化人的属性"""
        self.name = ""
        self.age = 0
        self.sex = ""
        self.face_encoding = np.array([])

    def get_current_face_encoding(self):
        """获取现在的face_encoding"""
        vc = VideoCapture()
        vc.read_frame()
        face_encodings = vc.get_face_encodings()
        while len(face_encodings) != 1:
            vc.read_frame()
            face_encodings = vc.get_face_encodings()
        self.face_encoding = face_encodings[0]
        vc.destroy_instance()


if __name__ == "__main__":
    print("people_info.py模块调试")
    pep = People()
    pep.get_current_face_encoding()
    print(pep.face_encoding)




