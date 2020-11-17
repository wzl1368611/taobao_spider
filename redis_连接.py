import redis
# 建立连接
r = redis.Redis(host="127.0.0.1",port=6379,db=0)
# 设置键值
r.set("name","belief")
r.set("name_ch","信仰")
# 获取值，返回的是bytes类型数据
res = r.get("name")
# print(type(res))
# decode解码
res2 = r.get("name").decode()
# print(type(res2))
# 打印结果
print(res)
print(res2)
# 获取所有的key
print(r.keys())
# print(type(r.keys()))
# 遍历所有的key，打印key和value
for k in r.keys():
    # print(type(k))
    print("{k}:{v}".format(k=k.decode(),v=r.get(k).decode()))
# 获取n开头的key
print(r.keys("n*"))
