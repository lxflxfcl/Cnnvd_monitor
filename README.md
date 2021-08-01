# Cnnvd_monitor
### CNNVD漏洞信息监控脚本

基于Python爬虫的CNNVD漏洞信息监控脚本——Cnnvd_monitor，实现了对CNNVD官网平台的实时监控、数据获取、入库、并用微信进行实时推送、并将获取的数据进行Web端表格展示。

每五个小时检测一次，网站是否更新。

### 使用说明

首先进行数据库初始化，初始化时生成log文件夹用来存放生成的日志文件。命令如下：

```
python3 installDb.py
```

#### 配置企业微信推送

这个需要先到企业微信创建一个企业，并自建一个应用，**获取到自定义应用的 Secret和注册的企业 corpid**，就可以了。修改位置在**Cnnvd_moniter.py文件的161行至165行**

启动监控脚本，命令如下：

```
python3 Cnnvd_moniter.py
```

### 效果展示

![](doc/1.png)

点击卡片会跳转到Web表单展示页面，如下：

![](doc/2.png)

