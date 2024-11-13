from config import FUND_CODES, SEND_NORMAL_STATUS, ERROR_THRESHOLD
from fund_analyzer import get_recent_fund_data, check_fund_conditions, is_monthly_notification_time
from notification import AlertNotifier, ErrorNotifier, DailySummaryNotifier

def main():
    alert_notifier = AlertNotifier()
    error_notifier = ErrorNotifier()
    summary_notifier = DailySummaryNotifier()
    is_monthly_time = is_monthly_notification_time()

    # 检查是否需要发送每日汇总
    if summary_notifier.should_send_summary():
        summary_notifier.send_daily_summary()

    for fund_code in FUND_CODES:
        try:
            fund_data = get_recent_fund_data(fund_code)
            daily_decline, significant_drop = check_fund_conditions(fund_data)
            
            if daily_decline or significant_drop or SEND_NORMAL_STATUS or is_monthly_time:
                alert_notifier.send_fund_alert(fund_code, daily_decline, significant_drop, is_monthly_time)
                summary_notifier.add_record(fund_code, "alert", "触发预警条件")
            else:
                summary_notifier.add_record(fund_code, "normal", "运行正常")
            
            print(f"\n基金 {fund_code} 分析结果：")
            print(f"日跌幅超过1%: {daily_decline}")
            print(f"总跌幅超过5%: {significant_drop}")
            
        except Exception as e:
            error_msg = str(e)
            print(f"获取基金 {fund_code} 数据时出错：{error_msg}")
            
            error_count = error_notifier.handle_error(fund_code, error_msg)
            summary_notifier.add_record(fund_code, "error", error_msg)
            
            if error_count >= ERROR_THRESHOLD:
                error_notifier.send_error_alert(fund_code, error_count, error_msg)

if __name__ == "__main__":
    main()


