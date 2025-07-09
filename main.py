from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
import requests, os
import logging

logger = logging.getLogger("uvicorn.error")

app = FastAPI()

def check_cached_file(cached_file) -> bool:
    is_cached = os.path.exists(cached_file)
    return is_cached

def download_new_file(index_path, original_url, alpine_file, downloaded_file) -> bool:
    try:
        # Check index_path if existing
        is_existed = os.path.exists('cache' + index_path)
        if not is_existed:
            os.makedirs('cache' + index_path)

        # Check url if available
        response = requests.get(original_url)
        rcode = response.status_code

        # Download the index file
        if rcode == 200:
            logger.info("The url %s is available", original_url)
            logger.info("Downloading file %s...", alpine_file)
            with open(downloaded_file, "wb") as file:
                file.write(response.content)
                logger.info("Downloaded file %s successfully", alpine_file)
                return True
        else:
            logger.error("The url %s is not available (Return code: %s)", original_url, rcode)
            return False
    except Exception as e:
        logger.error("An error occurred: %s", e)
        return False

@app.get("/alpine/{version}/{channel}/{platform}/{alpine_file}")
async def proxy_alpine(request: Request, alpine_file: str, cache_dir='cache'):
    if os.path.exists(cache_dir): os.makedirs(cache_dir)
    required_file = cache_dir + request.url.path
    index_path = '/'.join(request.url.path.split("/")[:-1])
    original_url = "https://dl-cdn.alpinelinux.org" + request.url.path

    is_cached = check_cached_file(required_file)
    if is_cached:
        logger.info("File %s is cached => Returning the cached one.", required_file)
        return FileResponse(required_file)

    is_downloaded = download_new_file(index_path, original_url, alpine_file, required_file)
    if is_downloaded:
        logger.info("File %s is downloaded => Serving the downloaded one.", required_file)
        return FileResponse(required_file)

    return None