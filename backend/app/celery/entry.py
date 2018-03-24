import datetime
from celery import schedules, current_app
from celery.beat import ScheduleEntry
from celery.utils.time import is_naive

from app.extensions import db
from app.models import CrontabSchedule, IntervalSchedule, DatabaseSchedulerEntry


class Entry(ScheduleEntry):
	model_schedules = (
		(schedules.crontab, CrontabSchedule, "crontab"),
		(schedules.schedule, IntervalSchedule, "interval"),
	)

	def __init__(self, model):
		self.app = current_app._get_current_object()
		self.name = model.name
		self.task = model.task
		self.schedule = model.schedule
		self.args = model.args
		self.kwargs = model.kwargs
		self.options = dict(
			queue = model.queue,
			exchange = model.exchange,
			routing_key=model.routing_key,
			expires=model.expires,
			)
		self.total_run_count = model.total_run_count
		self.model = model

		if not model.last_run_at:
			model.last_run_at = self._default_now()
		orig = self.last_run_at = model.last_run_at
		if not is_naive(self.last_run_at):
			self.last_run_at = self.last_run_at.replace(tzinfo=None)
		
	def is_due(self):
		if not self.model.enabled:
			return False, 5.0
		return self.schedule.is_due(self.last_run_at)

	def _default_now(self):
		return datetime.datetime.utcnow()

	def __next__(self):
		self.model.last_run_at = self._default_now()
		self.model.total_run_count += 1
		db.session.commit()
		return self.__class__(self.model)
	next = __next__


	@classmethod
	def to_model_schedule(cls, schedule):
		for schedule_type, model_type, model_field in cls.model_schedules:
			schedule = schedules.maybe_schedule(schedule)
			if isinstance(schedule, schedule_type):
				model_schedule = model_type.from_schedule(dbsession, schedule)
				return model_schedule, model_field
			raise ValueError(
					'Cannot convert schedule type {0!r} to model'.format(schedule)
				)

	@classmethod
	def from_entry(cls, name, skip_fields=('relative', 'options'), **entry):
		options = entry.get('options') or {}
		fields = dict(entry)
		for skip_field in skip_fields:
			fields.pop(skip_field, None)
		schedule = fields.pop('schedule')
		model_schedule, model_field = cls.to_model_schedule(schedule)
		fields[model_field] = model_schedule
		fields['args'] = fields.get('args') or []
		fields['kwargs'] = fields.get('kwargs') or {}
		fields['queue'] = options.get('queue')
		fields['exchange'] = options.get('exchange')
		fields['routing_key'] = options.get('routing_key')

		query = DatabaseSchedulerEntry.query().filter_by(name=name)
		db_entry = query.first()
		if db_entry is None:
			new_entry = DatabaseSchedulerEntry(**fields)
			new_entry.name = name
			db.session.add(new_entry)
			db.session.commit()
			db_entry = new_entry
		return cls(db_entry)