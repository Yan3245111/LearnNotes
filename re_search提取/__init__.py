import re


str_list = ["3小时2分钟",
            "1天2小时5分钟",
            "4天3小时12分钟"]


all_minutes = 0
for i in str_list:
    days = re.search(r'(\d+)天', i)
    hours = re.search(r'(\d+)小时', i)
    minutes = re.search(r'(\d+)分钟', i)
    print(days, hours, minutes)

    if days:
        all_minutes += int(days.group(1)) * 24 * 60
    if hours:
        all_minutes += int(hours.group(1)) * 60
    if minutes:
        all_minutes += int(minutes.group(1))
