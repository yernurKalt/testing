import asyncio
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jobify import Jobify

UTC = ZoneInfo("UTC")
# 1. Initialize Jobify
app = Jobify(tz=UTC)


@app.task(cron="* * * * * * *")  # Runs every second
async def my_cron() -> None:
    print("Hello! cron running every second")


@app.task
def my_job(name: str) -> None:
    now = datetime.now(tz=UTC)
    print(f"Hello, {name}! job running at: {now!r}")


async def main() -> None:
    # 4. Run the Jobify application context
    async with app:
        # Run immediately in the background.
        job = await my_job.push("Alex")

        # Schedule a one-time job at a specific time.
        run_next_day = datetime.now(tz=UTC) + timedelta(days=1)
        job_at = await my_job.schedule("Connor").at(run_next_day)

        # Schedule a one-time job after a delay.
        job_delay = await my_job.schedule("Sara").delay(20)

        # Start a dynamic cron job.
        job_cron = await my_cron.schedule().cron(
            "* * * * *",
            job_id="dynamic_cron_idd",
        )

        await job_at.wait()
        await job_delay.wait()
        await job_cron.wait()
        # You can also use the `await app.wait_all()` method to wait for
        # all currently running jobs to complete.
        # Note: If there are infinitely running cron jobs, like `my_cron`,
        # `app.wait_all()` will block indefinitely until a timeout is set.
        # await app.wait_all()


if __name__ == "__main__":
    asyncio.run(main())