import asyncio

from jobify import Jobify

app = Jobify()


@app.task
def my_task(x: int, y: int) -> int:
    return x + y


async def main() -> None:
    async with app:
        # Scheduling a task returns a Job instance
        job = await my_task.schedule(1, 2).delay(1)
        print(f"Job {job.id} was scheduled.")
        await job.wait()  # Wait for this specific job to complete
        print(f"Job {job.id} finished with status: {job.status}")
        print(f"Result: {job.result()}")


if __name__ == "__main__":
    asyncio.run(main())