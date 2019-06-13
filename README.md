
## 接口格式
1. 接口一 

项目中令HOST=http://127.0.0.1:5000/

- url:`http://127.0.0.1/shorten`
- method: 'GET', 'POST'
- return: a dict like
```
{
    'status': 'success',
    'code': code,
    'host': HOST
} 
```

> - code 代表由用户请求的长链接生成的6为关键字码

> - HOST 表示服务所用的主机和端口



2. 接口二

- url:`http://127.0.0.1:5000/<code>`
- method: 'GET'
- return: 通过302重定向的长链接去


## 代码架构

基于tdd的flask短链接服务，并通过docker实现容器部署

### 代码层次结构
```
.
├── cache
├── config
├── db
├── docker-compose.yml
├── Dockerfile
├── htmlcov
├── manage.py
├── migrations
├── MyApp
├── nginx
├── Pipfile
├── Pipfile.lock
├── __pycache__
├── README.md
├── requirements.txt
├── tests
├── utils
└── 需求文档.md

```

### 测试覆盖率

```
Coverage Summary:
Name                    Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------
MyApp/__init__.py          16      8      0      0    50%
MyApp/views.py             58     46     16      4    24%
config/development.py       3      0      0      0   100%
config/production.py        3      0      0      0   100%
manage.py                  34     30      6      1    12%
---------------------------------------------------------
TOTAL                     114     84     22      5    27%

```

## 设计思路
接口一：
使用redis做缓存和发号器，redis中设置 一个自增key,每当一个新的url过来的时候`自增key+1`,生成code,将自增key,code,url保存到MySQL数据库中并在redis中存一份`code-->url`,和`url-->code`的映射表，时效为一天，那么当有一个url重复的去申请创建code的时候会从redis中读取。

接口二：当一个code从前端传过来的时候

1. 如果不符合6位的规范，回到生成页面
2. 如果code在缓存中，就取出对应的url,重定向到url,
3. 如果不在缓存中就有两种可能性。
    1. 原本在redis中过期了，那么就从数据库中取出url并重定向
    2. 不在redis也不在数据库中，回到生成页面


## 使用
```shell
export FLASK_APP=manage.py
pipenv install
# 启动服务器
python3 manage.py runserver
# 创建数据库
python3 manage.py recreate_db
# 测试
python3 manage.py test
# 测试覆盖率检测
python3 manage.py cov
# 容器运行
docker-compose up -d --build

```

## TODO
1. 持续集成
2. 分布式