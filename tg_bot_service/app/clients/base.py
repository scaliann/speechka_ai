from asyncio import sleep
from logging import getLogger
from typing import Any, Unpack

from aiohttp import ClientSession
from aiohttp.client import _RequestOptions
from aiohttp.client_exceptions import ClientResponseError
from aiohttp.web import HTTPConflict
from pydantic import BaseModel


_valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]
logger = getLogger(__name__)


class BaseClient:
    def __init__(self, host: str):
        self.host = host

    async def request(
        self,
        path: str,
        method: str = "GET",
        response_model: Any = None,
        retry: int = 3,
        **kwargs: Unpack[_RequestOptions],
    ) -> Any:
        """
        path: str - should start with '/'
        """
        if not path.startswith("/"):
            raise ValueError("Path should start with /")
        if method.upper() not in _valid_methods:
            raise ValueError(f"Invalid method {method}")
        if kwargs.get("data") or kwargs.get("json"):
            request_data = kwargs.get("data") or kwargs.get("json")
            logger.info(f"REQUEST: {method} {self.host}{path} {request_data}")
        else:
            logger.info(f"REQUEST: {method} {self.host}{path}")
        for _ in range(retry):
            try:
                async with ClientSession() as session:
                    response = await session.request(
                        method=method,
                        url=f"{self.host}{path}",
                        **kwargs,
                    )
                    if response_model and issubclass(response_model, BaseModel):
                        body = await response.json()
                        logger.info(
                            f"RESPONSE {method} {self.host}{path} "
                            f"STATUS: {response.status} BODY: {body}"
                        )
                        return response_model.model_validate(body)
                    body = await response.text()
                    logger.info(
                        f"RESPONSE {method} {self.host}{path} "
                        f"STATUS: {response.status} BODY: {body}"
                    )
                    return body
            except TimeoutError:
                continue
        raise TimeoutError(f"Request timeout for {method} {path}")

    async def request_file(
        self,
        url: str,
        method: str = "GET",
        retry: int = 3,
        retry_sleep: int = 5,
        **kwargs: Unpack[_RequestOptions],
    ) -> bytes:
        if method.upper() not in _valid_methods:
            raise ValueError(f"Invalid method {method}")
        logger.info(f"REQUEST FILE: {method} {url}")
        error = None
        for _ in range(retry):
            try:
                async with ClientSession() as session:
                    response = await session.request(
                        method=method,
                        url=url,
                        **kwargs,
                    )
                    logger.info(
                        f"RESPONSE {method} FILE {url} STATUS: {response.status}"
                    )
                    return await response.read()
            except TimeoutError:
                error = TimeoutError(f"Request timeout for {method} {url}")
            except ClientResponseError as err:
                error = err
                # Ошибка возникает, когда пытаемся прочитать файл, который только загружается
                if err.status == HTTPConflict.status_code:
                    await sleep(retry_sleep)
                    continue
                break

        raise error
