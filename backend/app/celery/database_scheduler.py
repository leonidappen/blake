import time

from celery.beat import Scheduler

from .entry import Entry
from app.extensions import db
from app.models import DatabaseSchedulerEntry


class DatabaseScheduler(Scheduler):
	Entry = Entry
	_last_timestamp = None
	_schedule = None
	_initial_read = False

	def __init__(self, app, **kwargs):
		self._last_timestamp = self._get_latest_change()
		Scheduler.__init__(self, app, **kwargs)

	def _get_latest_change(self):
		query = DatabaseSchedulerEntry.query.with_entities(DatabaseSchedulerEntry.date_changed)\
					.order_by(DatabaseSchedulerEntry.date_changed.desc())
		latest_entry_date = query.first()
		return latest_entry_date

	def setup_schedule(self):
		self.install_default_entries(self.schedule)
		self.update_from_dict(self.app.conf.CELERYBEAT_SCHEDULE)

	def _all_as_schedule(self):
		s = {}
		query = DatabaseSchedulerEntry.query.filter_by(enabled=True).all()
		for row in query:
			s[row.name] = Entry(row)
		return s

	def schedule_changed(self):
		ts = self._get_latest_change()
		if not ts:
			return False
		if ts > self._last_timestamp:
			self._last_timestamp = ts
			return True

	def update_from_dict(self, dict_):
		s = {}
		for name, entry in dict_.items():
			try:
				s[name] = self.Entry.from_entry(name, **entry)
			except Exception as exc:
				self.logger.exception('update_from_dict')
		self.schedule.update(s)

	def tick(self):
		self.logger.debug('DatabaseScheduler: tick')
		Scheduler.tick(self)
		if self.should_sync():
			self.sync()
		return 5  # sleep time until next tick

	def should_sync(self):
		sync_reason_time = (time.time() - self._last_sync) > self.sync_every
		sync_reason_task_count = self.sync_every_tasks and self._tasks_since_sync >= self.sync_every_tasks
		bool_ = sync_reason_time or sync_reason_task_count
		self.logger.debug('DatabaseScheduler: should_sync: {0}'.format(bool_))
		return bool_

	def sync(self):
		self._last_sync = time.time()
		self.logger.debug('DatabaseScheduler: sync')
		self._schedule = self._all_as_schedule()

	@property
	def schedule(self):
		update = False
		if not self._initial_read:
			self.logger.debug('DatabaseScheduler: intial read')
			update = True
			self._initial_read = True
		elif self.schedule_changed():
			self.logger.info('DatabaseScheduler: Schedule changed.')
			update = True

		if update:
			self.sync()
		return self._schedule