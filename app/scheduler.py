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

        while True:
            schedule.run_pending()
            time.sleep(1)

    def _safe_run(self):
        self.logger.info("Scheduled run started")
        try:
            self.job()
            self.logger.info("Scheduled run completed successfully")
        except Exception:
            self.logger.exception("Scheduled run failed")

