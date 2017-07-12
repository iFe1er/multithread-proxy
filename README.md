# multithread-proxy

python 2.7

Requirements:见requirements.txt
使用 
 pip install requirements -r
 安装所有依赖包
 
 需要使用的同学直接git clone下来用就好了，记得要下载对应版本的PhantomJS，并在第90行处修改一下可执行文件的路径！
 
 新功能：
多线程代理池：
1. 新增西刺代理(xicidaili)+快代理(kuaidaili)两个来源的上千个免费代理
2. 保证代理的时效性和质量，增加国内外代理的有效性认证(validation)
3. 认证过程采用多线程操作
4. 为了方便配置，不使用数据库，改成文件操作，认证成功的保存在本地的txt文档中。
