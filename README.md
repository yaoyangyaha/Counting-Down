# Counting-Down
![GitHub License](https://img.shields.io/github/license/yaoyangyaha/Counting-Down)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/yaoyangyaha/Counting-Down/latest)
![GitHub contributors](https://img.shields.io/github/contributors/yaoyangyaha/Counting-DOwn)
![GitHub last commit](https://img.shields.io/github/last-commit/yaoyangyaha/Counting-Down)
<br/>
![GitHub Repo stars](https://img.shields.io/github/stars/yaoyangyaha/Counting-Down)
![GitHub followers](https://img.shields.io/github/followers/yaoyangyaha)
![GitHub forks](https://img.shields.io/github/forks/yaoyangyaha/Counting-Down)

一个基于`vue.js`和`FastAPI`有趣的每日打卡比拼小网站

## 1.序言😂
### 为什么我要做这个项目🧐
我所在的几个QQ群，大家都会在零点争着抢第一个打卡，非常热闹。~~（我知道这很神金）~~ 于是我想着能不能做一个更加专门用于打卡的网站来满足他们的 **“癖好”**。~~（我怎么感觉我更神金呢）~~。于是乎这个项目就诞生了，这个项目异常的简洁，因为他只有一个打卡功能 *（不排除我会在后期增加更多有意思的内容）*。

## 2.文件结构📁
```
Counting-Down/
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── requirements.txt
│   └── init.sql
│
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── index.js
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── views/
│   │   │   ├── Home.vue
│   │   │   ├── Login.vue
│   │   │   └── Register.vue
│   │   ├── App.vue
│   │   └── main.js
│   └── vite.config.js
│
└──init.sql
```
## 2.如何使用🤓
### 1.环境需要
MySQL >= 5.7.28\
Node >= v20.14.0\
npm >= 10.7.0\
Python >= 3.10\
***推荐使用上述环境（因为我只测试了这个版本下的可用性）***
### 2.构建前端
由于使用vue.js，因此需要使用npm构建
```bash
cd frontend
npm install
```
#### ⚠️注意！你需要根据情况修改你的前端部分代码
在`frontend/src/api/index.js`中将后端的`URL`修改为你的生产环境使用的后端使用的
在`frontend/src/views/Home.vue`中将`WebSocket`的`URL`修改成你的生产环境后端使用的
然后执行
```
npm run build
```
你可以获得静态文件

### 3.部署MySQL数据库
你只需要将`init.sql`查询表在数据库中执行即可

### 4.构建后端
安装需要的库（推荐使用`venv`虚拟环境）
```bash
cd backend
pip install -r requirements.txt
```
#### ⚠️你注意！你需要根据情况修改你的后端部分代码
在`db.py`中
```python
DATABASE_URL = "mysql+pymysql://checkin:123456@localhost:3306/checkin?charset=utf8mb4"
# 修改成你需要的mySQL数据库名称，账户，密码
```
在`auth.py`中
```python
SECRET_KEY = "<SECRET KEY>"
# 修改成你需要的SECRET_KEY，不要使用默认的，这非常不安全！！！
```
然后使用如下代码启用后端
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
### 大功告成！🎉
## 尾声😋
本项目遵循`MIT License`\
感谢各位的支持！欢迎大家fork项目、提交Issue和PR！
### 贡献者：
<a href="https://github.com/yaoyangyaha/Counting-Down/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yaoyangyaha/Counting-Down"  alt="Contributors"/>
</a>

### Buy Me A Coffee~
[ClickMe]("https://afdian.com/a/YAOYANGYAHA666")





