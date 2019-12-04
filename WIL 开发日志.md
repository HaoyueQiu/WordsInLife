### WIL 开发日志

#### ... - 20191127

1. 初步学习vue
2. debug 完成了注册和登录项目
3. 成功实现了导航守卫功能，当登录过后的用户跳转到登录界面时会被返回到原来界面，而未登录的用户会被强制跳转到登录界面。



#### 20191128

1. 将原始的httpAuth做的token生成验证改为jwt库实行生成验证功能，

   用户认证授权，原先使用flask-httpAuth实现的token功能，前端用户登录后不清楚自己的用户id，因此无法获取自己的信息。
   所以改用jwt库，它允许在token中添加一些不是隐私数据的payload。

2. 解决SQLite数据库默认无法删除列的问题，因为上一步修改了token列

   <https://stackoverflow.com/questions/30394222/why-flask-migrate-cannot-upgrade-when-drop-column>

   主要是修改env.py里面的配置

3. 解决了直接使用json截断token的问题，在js写了一个请求向flask后端调用了verify获取用户id





npm run dev命令崩溃，删掉node_module后npm i进行恢复



导航栏的逻辑理解，collapse会在界面较小时自动压缩,由于用显示器调试只使用一半屏幕，所以导航栏总是会被压缩，而不是什么奇奇怪怪的bug。



#### 20191129-30

1. 完整的登录注册功能，每次修改一点内容就会崩溃，简略模型。
2. profile功能先放个模板





#### 1202

1. profile之前get是通过id实现的，使用jwt不太会用axios发送get请求，所以会出现奇怪问题。缩减模型后user仅保留 username email name about_me字段，将username改为primary_key,将username存在window。localstorage中

2. 基础的词卡系统：创建了最基础的词类别和词卡模型

**计划**

先完成单词类别的瀑布流展示

1. 前端硬编码瀑布流展示
2. 从后端硬编码获取数据
3. 后端正常获取数据
4. 滚动

今晚完成了第一点，引入了vue-waterfall-easy插件，中间还是碰到挺多问题的，比如如何获取正确路径(static/img/...而不是从asset上获取)以及正确路径之后为什么不显示(插件position改为fixed)。

再完成点击类别进入到背单词界面中



#### 1204

debug完成了单词类别瀑布流展示功能，中间踩了一些坑，绕来绕去，最后终于解决了。

详见 vue瀑布流踩坑记



用户头像，个人主页

实现登录、登出

词卡系统

基础的词卡系统



用户 & 单词关联：

熟练度



词卡models：单词、音标、词意、例句、图片，单词号索引

词卡类别：图片，类别名称



点击词卡类别，根据熟练度从高到低排序