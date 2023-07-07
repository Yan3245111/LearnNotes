# ssh: connect to host github.com port 22: Connection timed out/refused

* 检查连接 ssh -T git@github.com
* 原因：电脑或者某个地方防火墙阻止
* 解决办法 将端口22更改为443
* 进入 .ssh文件新建config.txt，粘贴以下内容
```commandline
Host github.com
User 你的邮箱
Hostname ssh.github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa
Port 443
```
* 进入电脑右上角导航栏 查看->显示->文件扩展名
* 将confit后缀删除
* 重新执行ssh -T git@github.com
* 输入yes即可
