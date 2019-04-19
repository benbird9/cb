import tushare as ts

stock = ts.get_realtime_quotes('300058')
history = ts.get_today_ticks('300058')

print stock
print history
