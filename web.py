from flask import Flask,request
import sys, os, telnetlib, re, time

app = Flask(__name__)     #注意此处是两个下划线

def accessTel(tel,username, password):
    tel.read_until(b'Username:')
    tel.write(username.encode() + b'\n')
    tel.read_until(b'Password:')
    tel.write(password.encode() + b'\n')

def arp(ip,mac,area):#绑定ip与mac
    print(ip+' '+mac+' '+area)
    tel = telnetlib.Telnet("x.x.x.x")#交换机ip
    accessTel(tel,'username', 'password')#输入对应交换机账号密码
    tel.read_until(b'>')
    if area in ("aa","bb"):#判断地区选择对应交换机
        tel.write(b'telnet x.x.x.x' + b'\n')
    else:
        tel.write(b'telnet x.x.x.x' + b'\n')
    accessTel(tel,'username', 'password')
    tel.read_until(b'>')
    tel.write(b'sys' + b'\n')
    # 开始做指令
    tel.read_until(b']')
    tel.write(b'arp static ' + bytes(ip,'utf-8') + b' ' + bytes(mac,'utf-8') + b'\n')
    time.sleep(1)
    print(tel.read_very_eager().decode('ascii'))

    tel.close()

def undoarp(ip,area):#解绑ip与mac
    print(ip+' '+area)
    tel = telnetlib.Telnet("x.x.x.x")
    accessTel(tel,'username', 'password')
    tel.read_until(b'>')
    if area in ("aa","bb"):
        tel.write(b'telnet x.x.x.x' + b'\n')
    else:
        tel.write(b'telnet x.x.x.x' + b'\n')
    accessTel(tel,'username', 'password')
    tel.read_until(b'>')
    tel.write(b'sys' + b'\n')
    # 开始做指令
    tel.read_until(b']')
    tel.write(b'undo arp static ' + bytes(ip,'utf-8') + b'\n')
    time.sleep(1)
    print(tel.read_very_eager().decode('ascii'))

    tel.close()

@app.route('/')
def hello() -> str:
    return 'hello world!'

@app.route('/arp', methods = ['GET'])
def do_arp() -> 'str':
    ip = request.args.get('ip')
    mac = request.args.get('mac')
    area = request.args.get('area')
    mac=mac.replace(':','')#处理mac地址格式
    mac=mac.replace('-','')
    mac=mac.replace('/','')
    mac=mac.lower()
    arg=re.findall(r'.{4}',mac)
    mac='-'.join(arg)
    arp(ip,mac,area)
    results = 'OK'
    return results

@app.route('/undoarp', methods = ['GET'])
def undo_arp() -> 'str':
    ip = request.args.get('ip')
    area = request.args.get('area')
    undoarp(ip,area)
    results = 'OK'
    return results


app.run(host="0.0.0.0",port=5000)