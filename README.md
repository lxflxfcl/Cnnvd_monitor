# Cnnvd_monitor

## 更新

### 功能添加：

添加统计漏洞信息级别功能，七天统计一次，会在周五推送，并会显示在推送的消息卡片上。效果如下：

![](doc/3.jpg)

### BUG修复

修复因为token过期导致的微信卡片消息推送失败问题。

## CNNVD漏洞信息监控脚本

基于Python爬虫的CNNVD漏洞信息监控脚本——Cnnvd_monitor，实现了对CNNVD官网平台的实时监控、数据获取、入库、并用微信进行实时推送、并将获取的数据进行Web端表格展示。

感谢嘉隆师傅对代码进行完善修改。撒花。

每五个小时检测一次，网站是否更新。

## 使用说明

首先进行数据库初始化，初始化时生成log文件夹用来存放生成的日志文件。命令如下：

```
python3 installDb.py
```

### 配置企业微信推送

这个需要先到企业微信创建一个企业，并自建一个应用，**获取到自定义应用的 Secret和注册的企业 corpid**，就可以了。修改位置在**Cnnvd_moniter.py文件的161行至165行**

启动监控脚本，命令如下：

```
python3 Cnnvd_moniter.py
```

## 效果展示

![](doc/1.png)

点击卡片会跳转到Web表单展示页面，如下：

![](doc/2.png)

## 参考文章

https://blog.csdn.net/weixin_43345082/article/details/96475950

https://github.com/yhy0/github-cve-monitor

https://cloud.tencent.com/developer/article/1621016

**搜索引擎（debug）**