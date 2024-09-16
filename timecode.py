import time

#transform 1726502850.9138522 to 2024-09-01 12:00:50
def timecode_to_datetime(timecode):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timecode))

print(timecode_to_datetime(1726502850.9138522))