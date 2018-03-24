import json
import datetime

from app.extensions import db


class DatabaseSchedulerEntry(db.Model):
	__tablename__ = "celery_schedules"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	task = db.Column(db.Text)
	arguments = db.Column(db.Text, default="[]")
	keyword_arguments = db.Column(db.Text, default="{}")
	queue = db.Column(db.Text)
	exchange = db.Column(db.Text)
	routing_key = db.Column(db.Text)
	expires = db.Column(db.TIMESTAMP)
	enabled = db.Column(db.Boolean, default=True)
	last_run_at = db.Column(db.TIMESTAMP)
	total_run_count = db.Column(db.Integer, default=0)
	date_changed = db.Column(db.TIMESTAMP)
	celery_crontab_id = db.Column(db.Integer, db.ForeignKey("celery_crontabs.id"))
	celery_crontabs = db.relationship("CrontabSchedule", backref="celery_schedules")
	celery_interval_id = db.Column(db.Integer, db.ForeignKey("celery_intervals.id"))
	celery_intervals = db.relationship("IntervalSchedule", backref="celery_schedules")

	def __repr__(self):
		return "<DatabaseSchedulerEntry {}>".format(self)

	@property
	def args(self):
		return json.loads(self.arguments)

	@args.setter
	def args(self, value):
		self.arguments = json.dumps(value)
	
	@property
	def kwargs(self):
		return json.loads(self.keyword_arguments)

	@kwargs.setter
	def kwargs(self, kwargs_):
		self.keyword_arguments = json.dumps(kwargs_)

	@property
	def schedule(self):
		if self.celery_crontabs:
			return self.celery_crontabs.schedule
		if self.celery_intervals:
			return self.celery_intervals.schedule


@db.event.listens_for(DatabaseSchedulerEntry, "before_insert")
def _set_entry_cahnged_date(mapper, connection, target):
	target.date_changed = datetime.datetime.utcnow()