# 项目结构

.
├── app
│   ├── commands.py     // 一些可以通过命令行执行的命令
│   ├── errors.py       // 异常处理
│   ├── __init__.py     // 初始化对象app
│   ├── models.py       // 数据库表的定义
│   ├── static          // 前端静态文件
│   ├── templates       // 前端模板
│   └── views.py        // 视图函数


# 代码运行方式

首先在终端中进入项目文件夹，如果是第一次运行项目，需要依次执行以下命令：

```
flask initdb --drop  # 建表（加上`--drop`则先删除掉数据库中的所有表）
flask forge	# 生成虚拟数据
flask admin  # 设置管理员账号
```

通过以下命令运行项目：

`flask run`