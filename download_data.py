import baostock as bs
import pandas as pd

def today_date():
    import datetime
    today = datetime.datetime.today()
    return '{}-{}-{}'.format(today.year, today.month, today.day)

# start_date like
def download(file_path, code, start_date):
    # 登陆系统
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus(code,
                                      "date,code,open,high,low,close,preclose,volume,amount,pctChg",
                                      start_date=start_date, end_date=today_date(), frequency="d")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

    # 打印结果集
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    # 结果集输出到csv文件
    result.to_csv(file_path, index=False)

    # 登出系统
    bs.logout()

    print("download finished")


download("300.csv", "sh.000300", "2010-01-01")
