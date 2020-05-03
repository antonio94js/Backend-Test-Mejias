from datetime import date, timedelta

def get_future_day(offset = 10):
  return date.today() + timedelta(days=offset)