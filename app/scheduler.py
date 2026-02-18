import time
import schedule

class AutomationScheduler:
    def __init__(self, interval_minutes, job, logger):
        self.interval = interval_minutes
        self.job = job
        self.logger = logger

    def start(self):
        self.logger.info(
            f"Scheduler started (interval = {self.interval} minutes)"
        )

        schedule.every(self.interval).minutes.do(self._safe_run)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")

    def _safe_run(self):
        self.logger.info("Scheduled run started")
        try:
            self.job()
            self.logger.info("Scheduled run completed successfully")
        except Exception:
            self.logger.exception("Scheduled run failed")
