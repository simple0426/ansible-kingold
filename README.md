# 环境说明
* 远程主机(被控端)操作系统类型：Ubuntu
* Ansible使用版本：2.4

# 目录与文件说明
* environment：包含预上线和生产环境的主机列表及变量
* files：包含ansible跳板机的ssh配置文件及秘钥证书(已删除)
* roles：角色目录
* tasks：单独的任务目录
* ansible.cfg：自定义ansible配置文件
* deploy-xxx：零停机部署playbook
* site-xxx：代码部署playbook
* service-xxx：服务状态查看python脚本

# role目录说明
* common：新主机初始化
* db：安装mysql
    - deb方式安装
    - mysql版本：5.7.17
* haproxy：安装haproxy，haproxy配置文件更新
* interface_wechat_wm：interface_wechat_wm项目部署
* java：java项目环境配置
    - jdk
    - maven
    - supervisor
* java_project：java微服务项目部署
    - java项目框架spring cloud/eureka
* mgt_cop_user/mgt_user：mgt_cop_user/mgt_user【tomcat方式启动】项目部署
* nginx_conf：nginx配置文件管理
* project_java：java项目部署
    - java项目为spring boot框架
    - jar方式启动
* project_python：python项目部署
    - gunicorn方式启动python
    - python框架为flask
* project_web：web项目部署
* python：python项目环境配置
    - supervisor
    - flask
* service-core-product：java微服务service-core-product部署
* web：nginx安装与设置
* wechat/wechat_wm：前端项目wechat/wechat_wm部署
    - 前端框架：jquery、vue、nodejs

# 项目部署  
* 服务之间以逗号分隔
* 此处以预上线部署为例，生产环境部署只需将下列命令中的pre替换为prod

## 部署步骤
1. 代码部署：  
    - 通用部署：ansible-playbook -i environments/pre/hosts site-pre.yml -t 服务列表  
    - m站接口部署：ansible-playbook -i environments/pre/hosts site-pre.yml -t interface_wechat_wm -e "version=【tag】" 
    - 可用服务：除mgt_user/mgt_cop_user之外的全部服务
2. 服务零停机更新：  
    - 命令：ansible-playbook -i environments/pre/hosts deploy-pre.yml -t 服务列表
    - 可用服务：
        + java服务层(mgt_sms除外)
        + 微服务gateway
        + python接口服务
3. 代码回滚(根据需求执行)：
    - 一般回滚命令：ansible-playbook -i environments/pre/hosts deploy-pre.yml -t 服务列表 -e "rollback=true"
    - 快速回滚命令：ansible-playbook -i environments/pre/hosts deploy-pre.yml -t 服务列表 -e "rollback=true,end_sec=0,start_sec=0"

## 可用服务列表
* java服务层服务(15)
    - service_advisor
    - service_pfo
    - service_reward
    - service_fund
    - service_campaign
    - service_market
    - service_marketinfo
    - service_user
    - service_trade
    - service_product
    - service_base
    - service_organization
    - service_ifa
    - service_sms
    - service_coin
* 微服务(4)
    - framework-eureka-server
    - framework-gateway-server
    - framework-monitor-server
    - service-core-product
* java接口服务(9)
    - mgt_operation
    - mgt_user
    - mgt_cop_user
    - mgt_cop
    - mgt_fop
    - mgt_channel
    - mgt_kop
    - fop_auth
    - mgt_sms
* python接口服务(8)
    - interface_app
    - interface_campaign
    - interface_issuer
    - interface_notify
    - interface_wechat
    - interface_wechat_wm
    - interfact_ifa  
    - open_h5
    - open_api
* 前端项目(9)
    - cloud
    - cloud-h5
    - ifa
    - kingold-web
    - kop
    - web-kingold
    - wechat
    - wechat_wm
    - fop
