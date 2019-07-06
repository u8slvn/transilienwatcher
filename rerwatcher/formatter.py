from datetime import datetime

from loguru import logger
from lxml import etree


def calculate_time_delta_with_now(date, date_format):
    date = datetime.strptime(date, date_format)
    timedelta = date - datetime.now()

    return timedelta


def format_timedelta(timedelta):
    hours = timedelta.seconds // 3600
    minutes = (timedelta.seconds // 60) % 60
    minutes = 1 if minutes < 1 else minutes

    time = f"{minutes}min"
    time = f"{hours}h" if hours > 1 else time

    return time


class TimeTable:
    def __init__(self, miss, time):
        self.miss = miss
        self.time = time

    def text(self):
        return f"{self.miss}: {self.time}"

    def __str__(self):
        return f"TimeTable({self.text()})"


class TransilienApiFormatter:
    encoding = 'utf-8'
    date_format = '%d/%m/%Y %H:%M'

    def format_response(self, response, limit=2):
        if not response:
            return [TimeTable(miss='Error', time='api')]

        try:
            logger.info(f"Formatting response.")
            timetables = self._format_response(
                response=response,
                limit=limit
            )
        except Exception:
            logger.error(f"Formatting data failed.")
            return [TimeTable(miss='Error', time='format')]

        return timetables

    def _format_response(self, response, limit):
        response_body = response.text.encode(self.encoding)

        tree = etree.fromstring(response_body)
        trains = tree.xpath('/passages/train')

        timetables = []

        for train in trains[:limit]:
            miss = train.find('miss').text
            date = train.find('date').text

            timedelta = calculate_time_delta_with_now(
                date=date,
                date_format=self.date_format
            )
            time = format_timedelta(timedelta=timedelta)

            timetable = TimeTable(miss=miss, time=time)

            timetables.append(timetable)

        return timetables
