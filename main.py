import datetime
import backtrader as bt
import backtrader.feeds as btfeeds

class MyStrategy(bt.Strategy):

    def __init__(self):
        pass

    def next(self):
        if len(self) < 3:
            return

        last_open = self.data_open[-1]
        last_close = self.data_close[-1]
        change_rate = last_close / last_open
        if change_rate > 1.01:
            self.buy()
        elif change_rate < 0.997:
            self.close()

    def notify_order(self, order):
        print(order)


if __name__ == '__main__':
    cerebro = bt.Cerebro()

    cerebro.addstrategy(MyStrategy)

    data0 = btfeeds.GenericCSVData(
        dataname="300.csv",
        fromdate=datetime.datetime(2020, 1, 1),
        todate=datetime.datetime(2022, 12, 31),
        nullvalue=0.0,
        dtformat=('%Y-%m-%d'),
        datetime=0,
        high=3,
        low=4,
        open=2,
        close=5,
        volume=7,
        openinterest=9
    )

    startcash = 1000000
    cerebro.addsizer(bt.sizers.AllInSizer, percents=90)
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(0.00025)
    cerebro.adddata(data0)

    # 运行回测系统
    results = cerebro.run()

    # 获取回测结束后的总资金
    portvalue = cerebro.broker.getvalue()
    profit = portvalue - startcash
    # 打印结果
    print(f'总资金: {round(portvalue, 2)}')
    print(f'净收益: {round(profit, 2)}')
    cerebro.plot()
