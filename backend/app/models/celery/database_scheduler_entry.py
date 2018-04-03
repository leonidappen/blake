import json
import datetime

from sqlalchemy import Column, Integer, Text, TIMESTAMP, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.event import listens_for

from ..base import base


class DatabaseSchedulerEntry(base):
	__tablename__ = "celery_schedules"

	id = Column(Integer, primary_key=True)
	name = Column(Text)
	task = Column(Text)
	arguments = Column(Text, default="[]")
	keyword_arguments = Column(Text, default="{}")
	queue = Column(Text)
	exchange = Column(Text)
	routing_key = Column(Text)
	expires = Column(TIMESTAMP)
	enabled = Column(Boolean, default=True)
	last_run_at = Column(TIMESTAMP)
	total_run_count = Column(Integer, default=0)
	date_changed = Column(TIMESTAMP)
	celery_crontab_id = Column(Integer, ForeignKey("celery_crontabs.id"))
	celery_crontabs = relationship("CrontabSchedule", backref="celery_schedules")
	celery_interval_id = Column(Integer, ForeignKey("celery_intervals.id"))
	celery_intervals = relationship("IntervalSchedule", backref="celery_schedules")

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


@listens_for(DatabaseSchedulerEntry, "before_insert")
def _set_entry_cahnged_date(mapper, connection, target):
	target.date_changed = datetime.datetime.utcnow()