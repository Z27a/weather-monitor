from datetime import *
import time

# Using current time
ini_time_for_now = datetime.now()

# printing initial_date
print("initial_date", str(ini_time_for_now))

# Calculating future dates
# for two years
future_date_after_2yrs = ini_time_for_now + timedelta(days=730)

future_date_after_2days = ini_time_for_now + timedelta(days=2)

future_date_after_5min = ini_time_for_now + timedelta(minutes=5)

# printing calculated future_dates
# print('future_date_after_2yrs:', str(future_date_after_2yrs))
# print('future_date_after_2days:', str(future_date_after_2days))
#
# print(datetime.timestamp(ini_time_for_now), datetime.timestamp(future_date_after_5min))
#
# print(datetime.fromtimestamp(int(1589602450.825839)),datetime.fromtimestamp(1589602750.825839))

s = "2020-05-07"
s = s.replace('-','/')

print(int(time.mktime(datetime.strptime(s, '%Y/%m/%d').timetuple())))