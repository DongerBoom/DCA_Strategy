# DCA_Strategy

本项目采用定期运行的方式，更新关注的基金净值数据变动，基金净值达到预设指标时，用户会第一时间收到微信通知，便于及时进行交易。

## 功能特点

- 基金净值监控：实时跟踪关注基金的净值变动
- 自动预警：当基金净值达到预设的跌幅阈值时自动发送微信通知
- 定投提醒：每月固定时间发送定投提醒通知
- 每日汇总：每天晚上定时发送基金表现汇总
- 错误监控：监控程序运行状态,发生异常时通知

## 配置说明

在 config.py 中配置以下参数:

- FUND_CODES: 需要监控的基金代码列表
- GROSS_PRICE_DEC: 总跌幅预警阈值(默认5%)
- SINGLE_PRICE_DEC: 单日跌幅预警阈值(默认1%) 
- PUSHPLUS_TOKEN: 微信推送使用的token
- MONTHLY_INVESTMENT_DAY: 每月定投提醒日期
- MONTHLY_INVESTMENT_HOUR: 定投提醒时间(24小时制)
- DAILY_SUMMARY_HOUR: 每日汇总时间(默认20点)

## 使用方法

1. 安装依赖
~~~bash
pip install akshare request
~~~

2. 配置微信通知
需要被通知微信账号登陆https://www.pushplus.plus/
获取token补充在config.py PUSHPLUS_TOKEN

3. 运行main.py

4. 配置自动运行
参照项目提供的run_fund_monitor.sh配置linux自动运行脚本
~~~bash
chmod +x run_fund_monitor.sh
crontab -e
~~~
添加定时任务
~~~bash
# 每小时执行一次
0 * * * * /path/to/your/project/run_fund_monitor.sh

# 或者更详细的设置：
# 每个工作日（周一到周五）的 9:30 到 15:00 每小时执行一次
30 9-15 * * 1-5 /path/to/your/project/run_fund_monitor.sh
~~~


## 通知说明

系统会在以下情况发送通知：

1. 基金日跌幅超过设定阈值（默认1%）
2. 基金总跌幅超过设定阈值（默认5%）
3. 每月定投提醒，并汇总当月报警情况（可配置日期和时间）
4. 每日运行状况汇总（晚8点）
5. 连续获取数据失败警告

## 文件说明

- `main.py`: 主程序入口
- `config.py`: 配置文件
- `fund_analyzer.py`: 基金数据分析模块
- `notification.py`: 通知处理模块
- `run_fund_monitor.sh`: 运行脚本

