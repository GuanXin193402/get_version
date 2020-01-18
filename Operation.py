from linux_os import Linux
import re
import os
import shutil
import time
file_list=[] #文件清单
res={}#提取文件内容保存为字典
now_time=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
data={"省检修-南充分部550kV":{"中控":'867394040084765',
                             "人脸":'3GKL28XKYD'},
      "省检修-输电中心": {"中控": '867394040089673',
                        "人脸": ''},
      "南充-松林供电所":{"中控":'863412044475427',
                             "人脸":'3GKL2FC5YQ'},
      "雅安-500kV变电站":{"中控":'864388046445692',
                             "人脸":'3GKL2DE49J'},
      "绵阳-500kV诗城变电站":{"中控":'867394040052937',
                             "人脸":'3GKL2DGDP4'},
      "彭州-500kV丹景变电站":{"中控":'867394040080771',
                             "人脸":'3GKL2G15MF'},
      "西昌-500kV月城变电站":{"中控":'867394040101171',
                             "人脸":'3GKL2QOZZG'},
      "自贡-办公基地":{"中控":'867394040055542',
                             "人脸":'3GKL2QTFYR'},
      "自贡-500kV洪沟变电站":{"中控":'867394040014200',
                             "人脸":'3GKL2E1N86'},
      "自贡-500kV内江变电站":{"中控":'867394040052366',
                             "人脸":'3GKL2I7H7U'}
      # "省检修-南充分部550kV":{"中控":'867394040084765',
      #                        "人脸":'3GKL28XKYD'},
      # "省检修-南充分部550kV":{"中控":'867394040084765',
      #                        "人脸":'3GKL28XKYD'}
      }
remote_path=r'/root/version'
local_path=r'D:\桌面\version'
res_path=local_path+r'\result.txt'
try:
    if os.path.exists(local_path):
        shutil.rmtree(local_path)#删除目录
        time.sleep(2)
    if not os.path.exists(local_path):
        os.mkdir(local_path)#创建目录
except Exception as e:
    print(e)
    raise exit()
try:
    ps=input("请输入密码： ")
    host=Linux(ps)
    host.connect()#打开链接
    host.send(r"\cp -f $(find /home/docker/ksync/cd_tool -name '*VersionInfo.txt') /root/version",'#')#将cd_tool文件拷贝到version目录
    host.send(r"\cp -f $(find /home/docker/ksync/rfid_face -name '*VersionInfo.txt') /root/version",'#')#将rfid_face文件拷贝到version目录
    host.send(r"\cp -f $(find /home/docker/ksync/nc_tool -name '863412044475427-VersionInfo.txt') /root/version",'#')  # 将rfid_face文件拷贝到version目录
    file=host.send(r"ls /root/version",'#')#获取原始文件清单
    f=re.findall('.*.txt?',file)
    for i in f:
        a=i.split()
        for j in a:
            if 'null' not in j:
                file_list.append(j)#处理后获得纯净清单
    [host.ftp(remote_path,local_path,k) for k in file_list]#将文件从linux传输到windows下
except Exception as e1:
    print(e1)
    raise exit()
#file_list=['3GKL24QT7V-VersionInfo.txt', '865847044042354-VersionInfo.txt', '3GKL274AXN-VersionInfo.txt', '867394040014200-VersionInfo.txt', '3GKL2DE49J-VersionInfo.txt', '867394040052366-VersionInfo.txt', '3GKL2DGDP4-VersionInfo.txt', '867394040052937-VersionInfo.txt', '3GKL2E1N86-VersionInfo.txt', '867394040055542-VersionInfo.txt', '3GKL2I7H7U-VersionInfo.txt', '867394040080771-VersionInfo.txt', '3GKL2QOZZG-VersionInfo.txt', '867394040084765-VersionInfo.txt', '3GKL2QTFYR-VersionInfo.txt', '867394040085994-VersionInfo.txt', '3GKL2S60H2-VersionInfo.txt', '867394040089673-VersionInfo.txt', '3GKL2ZWJ0U-VersionInfo.txt', '867394040101171-VersionInfo.txt', '864388046445692-VersionInfo.txt', '867977030894902-VersionInfo.txt', '864583042036491-VersionInfo.txt']
try:
    for f in file_list:
        with open(os.path.join(local_path,f),'r',encoding='utf-8') as k:
            res[re.sub(r'-.*$', '', f)] = {'Time':k.readline(),
                                          'Version':re.sub(r'^.*：','',k.readline())}#处理文件获得信息字典
#    print(res)
except Exception as e2:
    print(e2)
    raise exit()
if not os.path.isfile(res_path):
    with open(res_path, 'a') as r:
        r.write("\t\t\t\t\t\t\t\t\t%s\t\t\t\t\t\t\t\t\t\n"%now_time)
        r.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
        r.write("|\t库房\t\t|\t中控ID\t\t|\t中控版本\t|\t上次更新时间\t|\t人脸ID\t\t|\t人脸版本\t|\t上次更新时间\t|\n")
        r.write("------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")  # 初始化结果文件r
try:
    for key,value in data.items():
        warehouse=key.strip().rjust(16,' ')
        for key1,value1 in data[key].items():
            if key1 =='中控':
                control_id=value1
            if key1 == '人脸':
                face_id=value1
        if control_id in res.keys():
            control_id_value=res[control_id].get('Version').strip().rjust(16,' ')
            control_id_time=res[control_id].get('Time').strip().rjust(16,' ')
        else:
            control_id_value='从未上报'.ljust(18,' ')
            control_id_time='从未上报'.ljust(18,' ')
        if face_id in res.keys():
            face_id_value = res[face_id].get('Version').strip().rjust(16,' ')
            face_id_time=res[face_id].get('Time').strip().rjust(16,' ')
        else:
            face_id_value = '从未上报'.ljust(18,' ')
            face_id_time='从未上报'.ljust(18,' ')
        with open(res_path,'a') as r:
            r.write(warehouse+'\t|'+control_id.rjust(12,' ')+'\t|'+control_id_value+'\t|'+control_id_time+'\t|'+face_id.rjust(16,' ')+'\t|'+face_id_value+'\t|'+face_id_time+'\n')
except Exception as e3:
    print(e3)
    raise exit()
host.close()#关闭链接