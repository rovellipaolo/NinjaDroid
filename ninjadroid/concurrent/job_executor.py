from concurrent.futures import ThreadPoolExecutor, Future


class JobExecutor:
    POOL_SIZE = 4
    executor = ThreadPoolExecutor(POOL_SIZE)

    def get(self) -> ThreadPoolExecutor:
        return self.executor

    def submit(self, job) -> Future:
        return self.executor.submit(job)
