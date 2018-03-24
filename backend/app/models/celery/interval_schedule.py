from datetime import timedelta

from celery import schedules

from app.extensions import db


class IntervalSchedule(db.Model):
	__tablename__ = "celery_intervals"

	id = db.Column(db.Integer, primary_key=True)
	every = db.Column(db.Integer, nullable=False)
	period = db.Column(db.Text)

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