import time
import schedule

MAX_RETRIES = 3
BASE_DELAY = 2  # seconds


class AutomationScheduler:
    def __init__(self, interval_minutes, job, logger):
        self.interval = interval_minutes
        self.job = job
        self.logger = logger

        self.success_count = 0
        self.failure_count = 0
        self._running = False

    def start(self):
        self.logger.info(
            f"Scheduler started (interval = {self.interval} minutes)"
        )

        # Run immediately once
        self._safe_run()

        schedule.every(self.interval).minutes.do(self._safe_run)

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped by user")

    def _safe_run(self):
        if self._running:
            self.logger.warning(
                "Previous run still active. Skipping this cycle."
            )
            return

        self._running = True
        self.logger.info("Scheduled run started")

        attempt = 0
        while attempt < MAX_RETRIES:
            try:
                self.job()
                self.success_count += 1
                self.logger.info(
                    "Scheduled run completed successfully"
                )
                break
            except Exception:
                attempt += 1
                if attempt < MAX_RETRIES:
                    delay = BASE_DELAY * (2 ** (attempt - 1))
                    self.logger.warning(
                        f"Run failed (attempt {attempt}/{MAX_RETRIES}). "
                        f"Retrying in {delay} seconds."
                    )
                    time.sleep(delay)
                else:
                    self.failure_count += 1
                    self.logger.exception(
                        "Run failed after maximum retries"
                    )

        self.logger.info(
            f"Metrics → Success: {self.success_count}, "
            f"Failures: {self.failure_count}"
        )

        self._running = False
