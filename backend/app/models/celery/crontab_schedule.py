from sqlalchemy import Column, Integer, Text
from celery import schedules

# from app.extensions import db
from ..base import base


class CrontabSchedule(base):
	__tablename__ = "celery_crontabs"

	id = Column(Integer, primary_key=True)
	minute = Column(Text, default="*")
	hour = Column(Text, default="*")
	day_of_week = Column(Text, default="*")
	day_of_month = Column(Text, default="*")
	month_of_year = Column(Text, default="*")
	
	@property
	def schedule(self):
		return schedules.crontab(
					minute=self.minute,
					hour=self.hour,
					day_of_week=self.day_of_week,
					day_of_month=self.day_of_month,
					month_of_year=self.month_of_year
				)

	@classmethod
	def from_schedule(cls, schedule):
		spec = {
			"minute": schedule._orig_minute,
			"hour": schdeule._orig_hour,
			"day_of_week": schedule._orig_day_of_week,
			"day_of_month": schedule._orig_day_of_month,
			"month_of_year": shedule._orig_month_of_year,
		}
		
		query = CrontabSchedule.query().filter_by(**spec).one_or_none()
		if query:
			return query
		return cls(**spec)
		