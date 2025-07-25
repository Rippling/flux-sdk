from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from functools import cache
from io import StringIO
from ssl import SSLContext, create_default_context
from threading import Lock
from typing import Iterable, Tuple
from urllib.parse import urlparse, urlunparse

import pyrfc3339
import requests
from google.protobuf.timestamp_pb2 import Timestamp
from requests.auth import _basic_auth_str
from requests.sessions import HTTPAdapter
from twirp.context import Context
from urllib3 import ProxyManager

from flux_sdk.utils.flux_proxy.flux.proxy.v1.proxy_pb2 import (
    EndSessionRequest,
    GetCACertificatesRequest,
    GetCACertificatesResponse,
    HttpHeader,
    StartSessionRequest,
    StartSessionResponse,
)
from flux_sdk.utils.flux_proxy.proxy_twirp import FluxProxyServiceClient

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SessionSettings:
    allow_hosts: Iterable[str] = field(default_factory=list)
    """
    Optional list of allowed hosts that the proxy will let this session connect to.  Defaults to allowing all hosts if
    unset.
    """

    credential_ids: Iterable[str] = field(default_factory=list)
    """
    Optional list of credential IDs to associate with outbound requests.
    """

    headers: dict[str, Iterable[str]] = field(default_factory=dict)
    """
    Optional HTTP headers to include with outbound requests
    Note that the values should be iterable, even if there is only one value. On the other hand, if you want to include
    multiple values for a single header, you should provide a list of values instead of providiing a single value with 
    comma separated values.
    """

    duration: timedelta = timedelta(hours=1)
    """
    The duration of the session, defaults to 1 hour if unset.
    """


class FluxProxyClient:
    """
    FluxProxyClient wraps the RPC interface of the Flux Proxy and also provides a convenience FluxProxySession that can
    be used to issue HTTP/S requests that pass through the proxy.
    """

    path_prefix: str = "/api"

    # todo : should provide a common instance of this based on configuration values.  in the future we can have multiple
    #        different proxies for different purposes.
    def __init__(self, ctlplane_addr: str, proxy_http_addr: str, proxy_https_addr: str):
        self.ctl_plane_addr: str = ctlplane_addr
        self.proxy_http_addr: str = proxy_http_addr
        self.proxy_https_addr: str = proxy_https_addr

    def start_session(self, settings: SessionSettings) -> FluxProxySession:
        """
        Initiates a session with the flux proxy.  Returns a FluxProxySession which is a subclass of requests.Session
        that sends all HTTP requests via the proxy.  The FluxProxySession is a context manaager, and if used as such,
        will automatically end the session on context exit.

        :return: the proxy session
        """
        session_id, secret = self._start_session(settings)
        return FluxProxySession(self, settings, session_id, secret)

    def _start_session(self, settings: SessionSettings) -> Tuple[str, str]:
        headers = [HttpHeader(name=k, values=[v] if isinstance(v, str) else v) for k, v in settings.headers.items()]

        resp: StartSessionResponse = self._svc(self.ctl_plane_addr).StartSession(
            ctx=Context(),
            request=StartSessionRequest(
                allow_hosts=settings.allow_hosts or [],
                credential_ids=settings.credential_ids or [],
                headers=headers if settings.headers else [],
                expires_at=_proto_time(datetime.now(tz=timezone.utc) + settings.duration),
            ),
            server_path_prefix=self.path_prefix,
        )
        return resp.session_id, resp.secret

    def end_session(self, session_id: str) -> None:
        """
        Ends the specified proxy session.  Failure is communicated via an exception.  The proxy will not report an error
        if requesting to delete a non-existent session.
        """
        self._svc(self.ctl_plane_addr).EndSession(
            ctx=Context(),
            request=EndSessionRequest(
                session_id=session_id,
            ),
            server_path_prefix=self.path_prefix,
        )

    @classmethod
    @cache
    def _svc(cls, ctlplane_addr: str) -> FluxProxyServiceClient:
        """
        this method is cached at the class level in case the client is doing things like managing connection pools.
        """
        return FluxProxyServiceClient(ctlplane_addr)

    @classmethod
    @cache
    def _load_ssl_context(cls, ctl_plane_addr: str) -> SSLContext:
        """
        this is an expensive method and is only needed once per proxy instance, so the return value is cached.
        """
        log.info(
            "retrieving CA cert from flux proxy",
            extra={
                "flux_proxy_addr": ctl_plane_addr,
            },
        )
        resp: GetCACertificatesResponse = cls._svc(ctl_plane_addr).GetCACertificates(
            ctx=Context(),
            request=GetCACertificatesRequest(),
            server_path_prefix=cls.path_prefix,
        )

        cadata = StringIO()
        for cert in resp.ca_certificates:
            cadata.write(cert)
            if not cert.endswith("\n"):
                cadata.write("\n")

        cadata.seek(0)
        return create_default_context(cadata=cadata.read())


class _FluxProxyAdapter(HTTPAdapter):
    def __init__(self, sess: FluxProxySession):
        super().__init__()
        self.sess: FluxProxySession = sess

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        """
        Integrates the Flux Proxy with the requests.Session.  This will plug in custom ProxyManagers that will pass the
        session information as an HTTP Basic header as well as wiring in the correct SSL context that honors the fake
        CA certificate.
        """
        ssl_context = self.sess.client._load_ssl_context(self.sess.client.ctl_plane_addr)
        headers = {"Proxy-Authorization": _basic_auth_str(self.sess.session_id, self.sess.secret)}
        if proxy in [self.sess.client.proxy_http_addr, self.sess.client.proxy_https_addr]:
            return ProxyManager(
                proxy,
                proxy_ssl_context=ssl_context,
                proxy_headers=headers,
                ssl_context=ssl_context,
            )
        raise Exception("unexpected proxy: " + proxy)


class FluxProxySession(requests.Session):
    """
    FluxProxySession extends requests.Session but pushes all traffic through the proxy.  It is a context manager and
    will end the session on context exit.  By default, it will automatically renew the session if expiration is
    imminent, allowing us to keep the session duration relativley short (default 1hr) while still supporting
    long-running tasks.
    """

    auto_renew_on_remaining = timedelta(minutes=1)

    def __init__(
            self, client: FluxProxyClient, settings: SessionSettings, session_id: str, secret: str,
            auto_renew: bool = True
    ):
        super().__init__()

        self.client: FluxProxyClient = client
        self.settings: SessionSettings = settings
        self.session_id: str = session_id
        self.secret: str = secret
        self.auto_rewew: bool = auto_renew
        self.lock = Lock()

        adapter = _FluxProxyAdapter(self)
        self.mount("http://", adapter)
        self.mount("https://", adapter)
        # this mapping is used by the requests adapter to determine if a proxy is required.  just using this facility
        # isn't enough b/c we need the adapater to plug in the SSL context.  however, without this mapping we never even
        # get to the point where it calls the `proxy_manager_for` func.  the hostname portion will be passed through to
        # `proxy_manager_for`, so it needs to match the values we're inspecting.
        self.proxies = {
            "http": self.client.proxy_http_addr,
            "https": self.client.proxy_https_addr,
        }

    def proxy_urls(self) -> Tuple[str, str]:
        """
        Returns a tuple with the HTTP proxy and HTTPS proxy (complete with BASIC auth) that can be provided to other
        processes as environment variables.  Can be used e.g. by flux to pass proxy information to Lambda functions.
        """
        return (
            self._insert_auth(self.client.proxy_http_addr),
            self._insert_auth(self.client.proxy_https_addr),
        )

    def _insert_auth(self, url_str: str) -> str:
        u = list(urlparse(url_str))
        u[1] = f"{self.session_id}:{self.secret}@{u[1]}"
        return urlunparse(u)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.client.end_session(self.session_id)
        except Exception as e:
            log.warn(
                "unable to close flux proxy session",
                extra={
                    "flux_proxy_session_id": self.session_id,
                    "flux_proxy_addr": self.client.ctl_plane_addr,
                    "error": e,
                },
            )

    def send(self, request, **kwargs):
        """
        Overrides the default implementation in requests.Session to add session renewal logic.  If session auto-renew is
        turned on, then each request is inspected to determine when the session is about to expire.  All the HTTP
        requests flow through this method, so it's a good single point to instrument.
        """

        resp = super().send(request, **kwargs)
        if not self.auto_rewew:
            return resp

        # this header may be missing in cases where we return with an error.
        sess_hdr = resp.headers.get("X-Flux-Session")
        if not sess_hdr:
            return resp

        sess_params = {
            parts[0]: parts[1] if len(parts) > 1 else ""
            for parts in [val.strip().split("=") for val in sess_hdr.split(",")]
        }
        expires_at = pyrfc3339.parser.parse(sess_params["expires_at"])
        if expires_at - datetime.now(tz=timezone.utc) < self.auto_renew_on_remaining:
            # assume that if another thread holds the mutex that auto-renew is getting taken care of.  we can continue
            # using a stale session/secret in the meantime since we don't end the session explicitly.
            if self.lock.acquire(blocking=False):
                try:
                    self.session_id, self.secret = self.client._start_session(self.settings)
                except Exception as e:
                    log.warn(
                        "unable to close renew proxy session",
                        extra={
                            "flux_proxy_session_id": self.session_id,
                            "flux_proxy_addr": self.client.ctl_plane_addr,
                            "error": e,
                        },
                    )
                finally:
                    self.lock.release()

        return resp


def _proto_time(dt: datetime) -> Timestamp:
    return Timestamp(seconds=int(time.mktime(dt.timetuple())))
