import requests
import time
import re
import random
import hmac
import hashlib
import math
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class CUC_Srun_Auth:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.tmot = 10  # 所有requests请求timeout时间
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/99.0.4844.51 Safari/537.36',
            'Host': 'net.cuc.edu.cn'
        }
        self.init_url = "https://net.cuc.edu.cn/"
        self.get_challenge_api = self.init_url + "cgi-bin/get_challenge"
        self.srun_portal_api = self.init_url + "cgi-bin/srun_portal"
        self.get_info_api = self.init_url + "cgi-bin/rad_user_info"
        self.n = "200"
        self.type = "1"
        self.ac_id = "5"
        self.enc = "srun_bx1"
        self.m = "1.12.4"
        self.ip = ""
        self.token = ""
        self.i = ""
        self.hmd5 = ""
        self.chksum = ""
        self.callback = "jQuery" + re.sub(r"\D", "", self.m + str(random.uniform(0, 1))) + "_" + str(
            int(time.time() * 1000))

    @staticmethod
    def force(msg):  # xencode
        ret = []
        for w in msg:
            ret.append(ord(w))
        return bytes(ret)

    @staticmethod
    def ordat(msg, idx):  # xencode
        if len(msg) > idx:
            return ord(msg[idx])
        return 0

    def sencode(self, msg, key):  # xencode
        l = len(msg)
        pwd = []
        for i in range(0, l, 4):
            pwd.append(
                self.ordat(msg, i) | self.ordat(msg, i + 1) << 8 | self.ordat(msg, i + 2) << 16
                | self.ordat(msg, i + 3) << 24)
        if key:
            pwd.append(l)
        return pwd

    @staticmethod
    def lencode(msg, key):  # xencode
        l = len(msg)
        ll = (l - 1) << 2
        if key:
            m = msg[l - 1]
            if m < ll - 3 or m > ll:
                return
            ll = m
        for i in range(0, l):
            msg[i] = chr(msg[i] & 0xff) + chr(msg[i] >> 8 & 0xff) + chr(
                msg[i] >> 16 & 0xff) + chr(msg[i] >> 24 & 0xff)
        if key:
            return "".join(msg)[0:ll]
        return "".join(msg)

    def get_xencode(self, msg, key):  # xencode
        if msg == "":
            return ""
        pwd = self.sencode(msg, True)
        pwdk = self.sencode(key, False)
        if len(pwdk) < 4:
            pwdk = pwdk + [0] * (4 - len(pwdk))
        n = len(pwd) - 1
        z = pwd[n]
        c = 0x86014019 | 0x183639A0
        q = math.floor(6 + 52 / (n + 1))
        d = 0
        while 0 < q:
            d = d + c & (0x8CE0D9BF | 0x731F2640)
            e = d >> 2 & 3
            p = 0
            while p < n:
                y = pwd[p + 1]
                m = z >> 5 ^ y << 2
                m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
                m = m + (pwdk[(p & 3) ^ e] ^ z)
                pwd[p] = pwd[p] + m & (0xEFB8D130 | 0x10472ECF)
                z = pwd[p]
                p = p + 1
            y = pwd[0]
            m = z >> 5 ^ y << 2
            m = m + ((y >> 3 ^ z << 4) ^ (d ^ y))
            m = m + (pwdk[(p & 3) ^ e] ^ z)
            pwd[n] = pwd[n] + m & (0xBB390742 | 0x44C6F8BD)
            z = pwd[n]
            q = q - 1
        return self.lencode(pwd, False)

    @staticmethod
    def get_sha1(value):  # sha1
        return hashlib.sha1(value.encode()).hexdigest()

    @staticmethod
    def get_md5(password, token):  # md5
        return hmac.new(token.encode(), password.encode(), hashlib.md5).hexdigest()

    @staticmethod
    def _getbyte(s, i):  # base64
        x = ord(s[i])
        if x > 255:
            logging.info("INVALID_CHARACTER_ERR: DOM Exception 5")
            logging.info(0)
        return x

    def get_base64(self, s):  # base64
        _PADCHAR = "="
        _ALPHA = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA"
        x = []
        imax = len(s) - len(s) % 3
        if len(s) == 0:
            return s
        for i in range(0, imax, 3):
            b10 = (self._getbyte(s, i) << 16) | (self._getbyte(s, i + 1) << 8) | self._getbyte(s, i + 2)
            x.append(_ALPHA[(b10 >> 18)])
            x.append(_ALPHA[((b10 >> 12) & 63)])
            x.append(_ALPHA[((b10 >> 6) & 63)])
            x.append(_ALPHA[(b10 & 63)])
        i = imax
        if len(s) - imax == 1:
            b10 = self._getbyte(s, i) << 16
            x.append(_ALPHA[(b10 >> 18)] + _ALPHA[((b10 >> 12) & 63)] + _PADCHAR + _PADCHAR)
        else:
            b10 = (self._getbyte(s, i) << 16) | (self._getbyte(s, i + 1) << 8)
            x.append(_ALPHA[(b10 >> 18)] + _ALPHA[((b10 >> 12) & 63)] + _ALPHA[((b10 >> 6) & 63)] + _PADCHAR)
        return "".join(x)

    def get_chksum(self):
        chkstr = self.token + self.username
        chkstr += self.token + self.hmd5
        chkstr += self.token + self.ac_id
        chkstr += self.token + self.ip
        chkstr += self.token + self.n
        chkstr += self.token + self.type
        chkstr += self.token + self.i
        return chkstr

    def get_info(self):
        info_temp = {
            "username": self.username,
            "password": self.password,
            "ip": self.ip,
            "acid": self.ac_id,
            "enc_ver": self.enc
        }
        i = re.sub("'", '"', str(info_temp))
        i = re.sub(" ", '', i)
        return i

    def init_getip(self):
        init_res = requests.get(self.init_url, headers=self.header, timeout=self.tmot)
        logging.info("初始化获取ip。")
        self.ip = re.search(r'ip\s*:\s"(.*?)",', init_res.text).group(1)
        logging.info("ip：" + self.ip)

    def get_token(self):
        get_challenge_params = {
            "callback": self.callback,
            "username": self.username,
            "ip": self.ip,
            "_": int(time.time() * 1000) + 1,
        }
        get_challenge_res = requests.get(self.get_challenge_api, params=get_challenge_params, headers=self.header,
                                         timeout=self.tmot)
        self.token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)
        logging.info("get_challenge_res：" + get_challenge_res.text)
        logging.info("token：" + self.token)

    def do_complex_work(self):
        info = self.get_info()
        self.i = "{SRBX1}" + self.get_base64(self.get_xencode(info, self.token))
        self.hmd5 = self.get_md5(self.password, self.token)
        self.chksum = self.get_sha1(self.get_chksum())
        logging.info("所有加密工作已完成。")

    def login(self):
        srun_portal_params = {
            'callback': self.callback,
            'action': 'login',
            'username': self.username,
            'password': '{MD5}' + self.hmd5,
            'ac_id': self.ac_id,
            'ip': self.ip,
            'chksum': self.chksum,
            'info': self.i,
            'n': self.n,
            'type': self.type,
            'os': 'Mac OS',
            'name': 'Macintosh',
            'double_stack': 0,
            '_': int(time.time() * 1000) + 1
        }
        logging.info('srun_portal_params：' + str(srun_portal_params))
        srun_portal_res = requests.get(self.srun_portal_api, params=srun_portal_params, headers=self.header,
                                       timeout=self.tmot)
        logging.info("srun_portal_res：" + srun_portal_res.text)

    def check_net(self):
        params = {
            "callback": "jQuery" + re.sub(r"\D", "", self.m + str(random.uniform(0, 1))) + "_" + str(
                int(time.time() * 1000)),
            '_': int(time.time() * 1000) + 1
        }
        res = requests.get(self.get_info_api, headers=self.header, params=params, timeout=self.tmot)
        net_status = re.search(r'"error":"(.*?)"', res.text).group(1)
        return net_status

    def main(self):
        if self.check_net() != 'ok':
            logging.info('未联网，准备联网。')
            self.init_getip()
            self.get_token()
            self.do_complex_work()
            self.login()
        else:
            logging.info('已联网。')


if __name__ == '__main__':
    csa = CUC_Srun_Auth()
    csa.main()
