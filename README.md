# CUC_Srun_Auth Python版
中国传媒大学校园网登录（深澜认证计费系统）Python版
## 简介
Python实现命令行登录中传校园网，目前仅宿舍和实验室有线网络端口可用，CUC-WiFi暂不需该系统登录。配合Mac、Linux系统的Crontab，Windows系统的“任务计划程序”，可实现断网自动登录。
## Inspiration
[huxiaofan1223/jxnu_srun](https://github.com/huxiaofan1223/jxnu_srun)，感谢这位大佬提供的深澜加密逻辑分析和代码实现。   
## 用法
```
git clone https://github.com/deweyshi/CUC_Srun_Auth.git
cd CUC_Srun_Auth
python CUC_Srun_Auth.py
```
记得先在“CUC_Srun_Auth.py”中填入自己的账号密码。   
self.username = “账号”   
self.password = “密码”
## 逻辑
大致逻辑是先通过登录接口检查是否联网状态，是则退出，不是则启动联网流程。
总体来说，联网涉及3次GET请求，第一次拿内网IP，第二次获取token，中间还涉及base64,md5,sha1,自有加密xencode，涉及的参数也很多，而且多种参数叠加很多加密，很容易晕。
## 贡献
主要的贡献是实现了callback的生成，这个主要是前端生成，从未登录的callback到登录完成截止是一个callback，登录完成后会立即生成新callback，用于查询联网状态。   
<img width="710" alt="Snipaste_2022-03-24_21-56-54" src="https://user-images.githubusercontent.com/39481369/159932291-11792750-13d8-42ff-8d72-2af1b24131d1.png">   
其实callback关键在于n.expando，expando关键在m，看似js文件有好多m，其实m必须是字符串，否则后面replace要报错，往上找找再结合抓包的数据就出来啦。
```
### all.main.js
...
m = "1.12.4",
...
expando: "jQuery" + (m + Math.random()).replace(/\D/g, ""),
...
jsonpCallback: function () {
    var a = jc.pop() || n.expando + "_" + Eb++;
    return this[a] = !0, a
}
...
```
# CUC_Srun_Auth JavaScript版
中国传媒大学校园网登录（深澜认证计费系统）JavaScript版
## 简介
实现访问认证页面即自动登录，需要配合Tampermonkey油猴插件等一同使用。
## 用法 
复制[代码](https://raw.githubusercontent.com/deweyshi/CUC_Srun_Auth/main/CUC_Srun_Auth.js)到[Tampermonkey](https://www.tampermonkey.net/)   
首次使用，先修改脚本中的账号和密码，之后可以顺畅自动登录。
