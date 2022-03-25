// ==UserScript==
// @name         中国传媒大学自动网络认证
// @namespace    https://github.com/deweyshi/CUC_Srun_Auth
// @version      0.1
// @description  首次使用先修改为自己的账号密码，之后即可以自动登录。
// @author       dayeshi
// @match        https://net.cuc.edu.cn/srun_portal_pc*
// @icon         https://www.cuc.edu.cn/_upload/tpl/00/56/86/template86/favicon.ico
// @grant        none
// @updateURL    https://raw.githubusercontent.com/deweyshi/CUC_Srun_Auth/main/CUC_Srun_Auth.js
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
    alert("首次使用，请修改脚本的第15、17行代码以添加自己的账号和密码。");
} else{
	document.getElementById("username").value = usr;
	document.getElementById("password").value = pwd;
	document.getElementById("login-account").click();
      }
})();
