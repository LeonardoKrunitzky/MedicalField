from src.strategies.base import SyncConflictStrategy


class LatestTimestampStrategy(SyncConflictStrategy):
    def resolve(self, local_record: dict, server_record: dict) -> dict:
        local_time = str(local_record.get("created_at", ""))
        server_time = str(server_record.get("created_at", ""))
        
        if local_time >= server_time:
            return local_record
        return server_record