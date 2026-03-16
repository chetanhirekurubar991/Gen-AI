from main import redis_client,logger
def on_library_update(library_name:str):
    pattern=f"chat:*{library_name}*"
    keys=redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)
        logger.info(f"Invalidated {len(keys)} cache keys for {library_name}")