from datetime import timedelta

from sqlalchemy import Column, Integer, Text
from celery import schedules

# from app.extensions import db
from ..base import base


class IntervalSchedule(base):
	__tablename__ = "celery_intervals"

	id = Column(Integer, primary_key=True)
	every = Column(Integer, nullable=False)
	period = Column(Text)

	@property
	def schedule(self):
		return schedules.schedule(timedelta(**{self.period: self.every}))

	@classmethod
	def from_schedule(cls, schedule, period="seconds"):
		every = max(schedule.run_every.total_seconds(), 0)

		query = IntervalSchedule.query().filter_by(every=every, period=period).one_or_none()
		if query:
			return query
		return cls(every=every, period=period)