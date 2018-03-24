from celery import schedules

from app.extensions import db


class CrontabSchedule(db.Model):
	__tablename__ = "celery_crontabs"

	id = db.Column(db.Integer, primary_key=True)
	minute = db.Column(db.Text, default="*")
	hour = db.Column(db.Text, default="*")
	day_of_week = db.Column(db.Text, default="*")
	day_of_month = db.Column(db.Text, default="*")
	month_of_year = db.Column(db.Text, default="*")
	
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
		