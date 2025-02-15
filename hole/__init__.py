"""*hole API Python client."""
import asyncio
import logging
import socket

import aiohttp
import async_timeout

from . import exceptions

_LOGGER = logging.getLogger(__name__)
_INSTANCE = '{schema}://{host}/{location}/api.php'


class Hole(object):
    """A class for handling connections with a *hole instance."""

    def __init__(self, host, loop, session, location='admin', tls=False,
                 verify_tls=True, api_token=None):
        """Initialize the connection to a *hole instance."""
        self._loop = loop
        self._session = session
        self.tls = tls
        self.verify_tls = verify_tls
        self.schema = 'https' if self.tls else 'http'
        self.host = host
        self.location = location
        self.api_token = api_token
        self.data = {}
        self.base_url = _INSTANCE.format(
            schema=self.schema, host=self.host, location=self.location)

    async def get_data(self):
        """Get details of a *hole instance."""
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(self.base_url)

            _LOGGER.info(
                "Response from *hole: %s", response.status)
            self.data = await response.json()
            _LOGGER.debug(self.data)

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from *hole: {}".format(self.host)
            _LOGGER.error(msg)
            raise exceptions.HoleConnectionError(msg)

    async def enable(self):
        """Enable DNS blocking on a *hole instance."""
        if self.api_token is None:
            _LOGGER.error("You need to supply an api_token to use this")
            return
        params = "enable=True&auth{}".format(self.api_token)
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(self.base_url,
                                                   params=params)

            _LOGGER.info(
                "Response from *hole: %s", response.status)
            data = await response.json()
            _LOGGER.debug(data)

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from *hole: {}".format(self.host)
            _LOGGER.error(msg)
            raise exceptions.HoleConnectionError(msg)


    async def disable(self, duration=True):
        """Disable DNS blocking on a *hole instance."""
        if self.api_token is None:
            _LOGGER.error("You need to supply an api_token to use this")
            return
        params = "disable={}&auth{}".format(duration, self.api_token)
        try:
            async with async_timeout.timeout(5, loop=self._loop):
                response = await self._session.get(self.base_url,
                                                   params=params)

            _LOGGER.info(
                "Response from *hole: %s", response.status)
            data = await response.json()
            _LOGGER.debug(data)

        except (asyncio.TimeoutError, aiohttp.ClientError, socket.gaierror):
            msg = "Can not load data from *hole: {}".format(self.host)
            _LOGGER.error(msg)
            raise exceptions.HoleConnectionError(msg)

    @property
    def status(self):
        """Return the status of the *hole instance."""
        return self.data['status']

    @property
    def unique_clients(self):
        """Return the unique clients of the *hole instance."""
        return self.data['unique_clients']

    @property
    def unique_domains(self):
        """Return the unique domains of the *hole instance."""
        return self.data['unique_domains']

    @property
    def ads_blocked_today(self):
        """Return the ads blocked today of the *hole instance."""
        return self.data['ads_blocked_today']

    @property
    def ads_percentage_today(self):
        """Return the ads percentage today of the *hole instance."""
        return self.data['ads_percentage_today']

    @property
    def clients_ever_seen(self):
        """Return the clients_ever_seen of the *hole instance."""
        return self.data['clients_ever_seen']

    @property
    def dns_queries_today(self):
        """Return the dns queries today of the *hole instance."""
        return self.data['dns_queries_today']

    @property
    def domains_being_blocked(self):
        """Return the domains being blocked of the *hole instance."""
        return self.data['domains_being_blocked']

    @property
    def queries_cached(self):
        """Return the queries cached of the *hole instance."""
        return self.data['queries_cached']

    @property
    def queries_forwarded(self):
        """Return the queries forwarded of the *hole instance."""
        return self.data['queries_forwarded']
