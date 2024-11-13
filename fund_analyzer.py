import akshare as ak
from datetime import datetime
from config import GROSS_PRICE_DEC, SINGLE_PRICE_DEC, MONTHLY_INVESTMENT_DAY, MONTHLY_INVESTMENT_HOUR

def get_recent_fund_data(fund_code):
    """获取基金最近的净值数据"""
    fund_data = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
    recent_data = fund_data.tail(22)
    return recent_data

def check_fund_conditions(fund_data):
    """检查基金是否满足预警条件"""
    latest_growth = fund_data['日增长率'].iloc[-1] / 100
    latest_nav = fund_data['单位净值'].iloc[-1]
    max_nav = fund_data['单位净值'].max()
    
    decline_rate = (max_nav - latest_nav) / max_nav
    
    is_daily_decline = latest_growth < -SINGLE_PRICE_DEC
    is_significant_drop = decline_rate > GROSS_PRICE_DEC
    
    return is_daily_decline, is_significant_drop

def is_monthly_notification_time():
    """检查是否是每月定投提醒时间"""
    now = datetime.now()
    return now.day == MONTHLY_INVESTMENT_DAY and now.hour == MONTHLY_INVESTMENT_HOUR