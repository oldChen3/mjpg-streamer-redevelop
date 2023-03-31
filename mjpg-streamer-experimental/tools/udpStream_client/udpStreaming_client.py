# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 10:38:39 2023

@author: chenjinghui
"""

import numpy as np
import socket
from PIL import Image
import cv2

udp_port = 554

def main():
    key = 0
    #  1.创建socket套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # AF_INET表示使用ipv4,默认不变，SOCK_DGRAM表示使用UDP通信协议
     
    #  2.绑定端口port
    local_addr = ("", udp_port)  # 默认本机任何ip ，指定端口号7878
    udp_socket.bind(local_addr)  # 绑定端口
     
    #  3.收发数据
    send_data = "udp_streaming_on"
    udp_socket.sendto(send_data.encode("utf-8"), ("192.168.0.8", 554))  # 编码成全球统一数据格式，用元组表示接收方ip和port
    while(ord('q') != key):
        len_data,port = udp_socket.recvfrom(4)
        recv_len = len_data[1]*256 + len_data[0]
        recv_data,port = udp_socket.recvfrom(1024*32)  # 定义单次最大接收字节数
        if(len(recv_data) != recv_len): #   如果长度和就收的数据长度不一致，则忽略此次数据包
            continue
        fd = open("img.jpg","wb+")
        fd.write(recv_data)
        fd.close()
        img = cv2.imread("img.jpg")
        img = cv2.resize(img, (0,0), fx=2, fy=2)
        cv2.imshow("video", img)
        key=cv2.waitKey(5)

    #  5.关闭套接字
    cv2.destroyAllWindows()
    udp_socket.close()
    
main()