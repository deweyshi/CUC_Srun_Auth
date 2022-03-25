// ==UserScript==
// @name         中国传媒大学自动网络认证
// @namespace    https://github.com/deweyshi/CUC_Srun_Auth
// @version      0.4
// @description  适用于中国传媒大学校园网认证登录（深澜认证计费系统），目前仅宿舍和实验室有线网络端口可用，CUC-WiFi暂不需该系统登录。首次使用先修改为自己的账号密码，之后即可以自动登录。
// @author       dayeshi
// @match        https://net.cuc.edu.cn/srun_portal_pc*
// @icon         https://www.cuc.edu.cn/_upload/tpl/00/56/86/template86/favicon.ico
// @grant        none
// @license      MIT
// ==/UserScript==
(function() {
    'use strict';
    // 首次使用请修改为自己的账号和密码⬇️
    // 账号⬇️
    var usr = "这填账号"
    // 密码⬇️
    var pwd = "这填密码"
    // 首次使用请修改为自己的账号和密码⬆️
if (usr === "这填账号" || pwd === "这填密码") {
    alert("首次使用，请先在脚本添加自己的账号和密码。");
} else{
	document.getElementById("username").value = usr;
	document.getElementById("password").value = pwd;
	document.getElementById("login-account").click();
      }
})();
