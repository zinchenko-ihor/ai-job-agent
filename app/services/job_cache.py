from datetime import datetime, timedelta


class JobCacheService:


    CACHE_HOURS = 6


    def should_refresh(
        self,
        last_collection_time
    ):

        if not last_collection_time:
            return True


        border = (
            datetime.utcnow()
            -
            timedelta(
                hours=self.CACHE_HOURS
            )
        )


        return last_collection_time < border
