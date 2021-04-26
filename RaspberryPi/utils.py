def add_minutes_to_time(time, minutes_to_add):
    hour = int(time.split(':')[0])
    minutes = int(time.split(':')[1])

    minutes += minutes_to_add
    if minutes >= 60:
        hour += 1
        minutes -= 60
        if hour > 23:
            hour = 0

    return str(hour) + ':' + str(minutes)


if __name__ == "__main__":
    print(add_minutes_to_time(time="23:52", minutes_to_add=18))
