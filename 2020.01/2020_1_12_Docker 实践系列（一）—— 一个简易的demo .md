
### 缘起
Docker 算是自己都想实践的方向之一，这个系列就记录一下自己学习的过程。

### Docker 介绍
Docker 是什么，网上的介绍很多，在这里我就不班门弄斧了，主要谈谈我对 Docker 的认识。

总体来看，Docker 是一个效率工具。
首先，使用 Docker 可以免去很多开发阶段令人头痛的配置问题；
其次，可以保证不同开发环节下，开发环境的一致性；
最后，Docker 的使用，使得程序的可移植性、横向拓展能力大幅提升，是云计算时代最重要的基础设施。

在这个时代，大量的基础设施和工具都是依赖于 Docker 而来，比如 CI/CD 的开发流程，比如 K8s 容器编排和管理。

我认为 Docker 是当代所有程序员都应该掌握的基本知识之一。

### Docker 实践的原则

- 每个 Docker 应该运行一个单独的应用，以 Web 应用为例，Web 服务 数据库 缓存 应该分别分别运行在各自的 Docker上。
有多个数据库，各个数据库也应该是一个单独的 Docker；

- 为每个 Docker 赋予适当的权限；

- 镜像层数尽可能少；

- 多个容器可以通过 Docker Compose 构建，避免维护管理各个容器之间的通信关系。

- Docker 不是虚拟机，容器中的应用都应该以前台执行，而不是像虚拟机、物理机里面那样，用 systemd 去启动后台服务，容器内没有后台服务的概念。

具体的可以参考：
https://yeasy.gitbooks.io/docker_practice/appendix/best_practices.html#%E4%B8%80%E8%88%AC%E6%80%A7%E7%9A%84%E6%8C%87%E5%8D%97%E5%92%8C%E5%BB%BA%E8%AE%AE

### 一个简单的 Docker 例子

服务描述：
一个 Flask 应用，可以记录并现实用户访问次数。
包含两个镜像 一个 Python 镜像和 Redis 镜像。
其中 Python 是使用官方 3.7.5 的镜像及本项目需要的库构建而成；
Redis 使用的官方默认的镜像。

两个镜像通过 Docker Compose 编排

环境信息：
Python版本：3.7.5
Web 框架：Flask
数据库： Redis

步骤一：创建项目文件


```
$ mkdir flask_docker_test
$ cd flask_docker_test
```

配置项目需要引入的包
```
# 创建 requirements.txt 文件，并写入需要引入的包名，默认安装最新版本
# flask_docker_test/requirements.txt
$ sudo vim requirements.txt
flask
redis
```

创建 Python 文件
```
$ sudo vim app.py

# flask_docker_test/app.py
from flask import Flask
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
```

步骤二：创建 Docker 镜像

镜像通过 Dockerfile 来创建

```
$ sudo vim Dockerfile
# flask_docker_test/Dockerfile

FROM python:3.7.5
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python app.py
EXPOSE 5000 # 对外暴露5000端口
```

解释：
FROM：以 Python 3.7.5 为基础构建镜像，Docker 会先查询本地有没有，这个版本的镜像，没有的话，会从官方的镜像去查询并下载。
ADD：复制 . /code 下的文件到 Docker 镜像中
WORKDIR： 指定工作目录
RUN：命令并创建新的镜像层
CMD：设置容器启动后默认执行的命令及其参数
EXPOSE：设置镜像启动后对外暴露的端口号


步骤三：通过 docker-compose.yml 来编排镜像及配置应用
```
$ sudo vim docker-compose.yml

version: '2'
services:
    web:
        build: .
        ports:
            - "5000:5000"
        volumes:
            - .:/code
        depends_on:
            - redis
    redis:
        image: redis
```

解释：



案例参考：
https://runnable.com/docker/python/docker-compose-with-flask-apps