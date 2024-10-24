import calendar
import datetime
import holidays

def next_friday():
    today = datetime.date.today()
    days_ahead = 4 - today.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return days_ahead

def next_holiday(country_code='US'):
    today = datetime.date.today()
    holiday_list = holidays.CountryHoliday(country_code, years=[today.year])
    final_result = None
    for date, name in holiday_list.items():
        if date > today:
            final_result = (date, name)
            break
    if not final_result:
        holiday_list = holidays.CountryHoliday(country_code, years=[today.year+1])
        for date, name in holiday_list.items():
            if date > today:
                final_result = (date, name)
                break
    return final_result

def days_until_date(date):
    today = datetime.date.today()
    days_until = (date - today).days
    return days_until

def days_until_next_month_day(day):
    today = datetime.date.today()
    year = today.year
    month = today.month + 1
    if month > 12:
        month = 1
        year += 1
    _, days_in_month = calendar.monthrange(year, month)
    next_month_day = datetime.date(year, month, day)
    
    if today < next_month_day:
        days_until = (next_month_day - today).days
    else:
        days_until = (datetime.date(year, month+1, day) - today).days

    return days_until

next_friday_days = next_friday()
print(f"Next Friday is {next_friday_days} days away.")

next_holiday_info = next_holiday(country_code='CN')
if next_holiday_info:
    holiday_date = next_holiday_info[0]
    holiday_name = next_holiday_info[1]
    print(f"The next holiday is {holiday_name} on {holiday_date}.")
else:
    print("There are no upcoming holidays.")

specific_date = datetime.date(2022, 12, 25)  # 指定日期为圣诞节
days_until_specific_date = days_until_date(specific_date)
print(f"There are {days_until_specific_date} days until {specific_date}.")
next_month_day = 10
days_until_next_month_day = days_until_next_month_day(next_month_day)
print(f"There are {days_until_next_month_day} days until the next {next_month_day}th of the month.")
