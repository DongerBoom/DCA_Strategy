import requests
import json
import os
from datetime import datetime
from config import PUSHPLUS_TOKEN, ALERT_HISTORY_FILE, ERROR_HISTORY_FILE, DAILY_SUMMARY_HOUR, DAILY_SUMMARY_FILE

def send_wechat(msg):
    """发送微信通知"""
    url = f"https://www.pushplus.plus/send"
    params = {
        'token': PUSHPLUS_TOKEN,
        'title': '定投通知',
        'content': msg,
        'template': 'html'
    }
    response = requests.get(url=url, params=params)
    print(response.text)
    return response.json()

class HistoryManager:
    @staticmethod
    def load_history(file_path):
        """加载历史记录"""
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {"count": 0, "events": []}

    @staticmethod
    def save_history(history, file_path):
        """保存历史记录"""
        with open(file_path, 'w') as f:
            json.dump(history, f)

class AlertNotifier:
    def __init__(self):
        self.history_manager = HistoryManager()

    def send_fund_alert(self, fund_code, daily_decline, significant_drop, is_monthly_time=False):
        """发送基金预警信息"""
        history = self.history_manager.load_history(ALERT_HISTORY_FILE)
        message = self._build_alert_message(fund_code, daily_decline, significant_drop, is_monthly_time, history)
        self.history_manager.save_history(history, ALERT_HISTORY_FILE)
        return send_wechat(message)

    def _build_alert_message(self, fund_code, daily_decline, significant_drop, is_monthly_time, history):
        if is_monthly_time:
            history.update({"count": 0, "events": []})
            return f"🔔 每月定投提醒：基金{fund_code}定投时间已到\n"
        
        if daily_decline or significant_drop:
            history["count"] += 1
            history["events"].append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "fund": fund_code,
                "daily_decline": daily_decline,
                "significant_drop": significant_drop
            })
            
            message = f"📊 本月第{history['count']}次预警\n"
            if daily_decline:
                message += f"⚠️ 基金{fund_code}日跌幅超过1%\n"
            if significant_drop:
                message += f"⚠️ 基金{fund_code}总跌幅超过5%\n"
            return message
        
        return f"✅ 基金{fund_code}运行正常，未触发任何预警条件\n"

class ErrorNotifier:
    def __init__(self):
        self.history_manager = HistoryManager()

    def handle_error(self, fund_code, error_msg):
        """处理错误并发送警报"""
        history = self.history_manager.load_history(ERROR_HISTORY_FILE)
        history["count"] += 1
        history["errors"].append({
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "fund": fund_code,
            "error": error_msg
        })
        self.history_manager.save_history(history, ERROR_HISTORY_FILE)
        return history["count"]

    def send_error_alert(self, fund_code, error_count, error_msg):
        """发送错误警报"""
        message = f"⚠️ 系统警告\n"
        message += f"基金{fund_code}连续{error_count}次获取数据失败\n"
        message += f"最新错误信息：{error_msg}\n"
        return send_wechat(message)

class DailySummaryNotifier:
    def __init__(self):
        self.history_manager = HistoryManager()

    def should_send_summary(self):
        """检查是否应该发送每日汇总"""
        now = datetime.now()
        return now.hour == DAILY_SUMMARY_HOUR and now.minute < 60

    def load_daily_records(self):
        """加载当日记录"""
        return self.history_manager.load_history(DAILY_SUMMARY_FILE)

    def save_daily_records(self, records):
        """保存当日记录"""
        self.history_manager.save_history(records, DAILY_SUMMARY_FILE)

    def add_record(self, fund_code, status, message):
        """添加运行记录"""
        records = self.load_daily_records()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if "date" not in records or records["date"] != today:
            records = {"date": today, "runs": [], "error_count": 0}
        
        records["runs"].append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "fund": fund_code,
            "status": status,
            "message": message
        })
        
        if status == "error":
            records["error_count"] += 1
            
        self.save_daily_records(records)

    def send_daily_summary(self):
        """发送每日汇总"""
        records = self.load_daily_records()
        today = datetime.now().strftime("%Y-%m-%d")
        
        if records.get("date") != today:
            return
        
        message = f"📊 {today} 基金监控日报\n"
        message += f"今日运行次数：{len(records['runs'])}\n"
        message += f"错误次数：{records['error_count']}\n\n"
        
        # 统计每个基金的情况
        fund_stats = {}
        for run in records["runs"]:
            fund_code = run["fund"]
            if fund_code not in fund_stats:
                fund_stats[fund_code] = {"alerts": 0, "errors": 0}
            
            if run["status"] == "alert":
                fund_stats[fund_code]["alerts"] += 1
            elif run["status"] == "error":
                fund_stats[fund_code]["errors"] += 1
        
        message += "基金详情：\n"
        for fund_code, stats in fund_stats.items():
            message += f"基金{fund_code}：触发预警{stats['alerts']}次，出错{stats['errors']}次\n"
        
        send_wechat(message)
        
        # 发送后清空记录
        self.save_daily_records({"date": today, "runs": [], "error_count": 0})