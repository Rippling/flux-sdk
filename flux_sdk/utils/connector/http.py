from http import HTTPStatus

from requests import Response

from flux_sdk.utils.exceptions import IntegrationDisconnectedException
from flux_sdk.utils.flux_proxy.flux_proxy import FluxProxyClient, FluxProxySession, SessionSettings


class HttpConnector:
    def __init__(self, credential_id: str):
        self.__client = FluxProxyClient(
            ctlplane_addr="http://flux-proxy.flux-proxy:8001",
            proxy_http_addr="http://flux-proxy.flux-proxy:80",
            proxy_https_addr="https://flux-proxy.flux-proxy:443",
        )
        self.__session: FluxProxySession = self.__initiate_session(credential_id=credential_id)

    def __del__(self):
        try:
            self.__client.end_session(self.__session.session_id)
        except Exception:
            ...

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    def __initiate_session(self, credential_id: str) -> FluxProxySession:
        return self.__client.start_session(SessionSettings(credential_ids=[credential_id]))

    def __raise_if_disconnected(self, response: Response) -> None:
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            disconnect_reason = ""
            raise IntegrationDisconnectedException(disconnect_reason=disconnect_reason)

    def get(self, url: str, **kwargs) -> Response:
        response: Response = self.__session.get(url=url, **kwargs)
        self.__raise_if_disconnected(response=response)
        return response

    def post(self, url: str, data=None, json=None, **kwargs) -> Response:
        response: Response = self.__session.post(url=url, data=data, json=json ** kwargs)
        self.__raise_if_disconnected(response=response)
        return response

    def put(self, url: str, data=None, **kwargs) -> Response:
        response: Response = self.__session.put(url=url, data=data, **kwargs)
        self.__raise_if_disconnected(response=response)
        return response

    def patch(self, url: str, data=None, **kwargs) -> Response:
        response: Response = self.__session.patch(url=url, data=data, **kwargs)
        self.__raise_if_disconnected(response=response)
        return response

    def delete(self, url: str, **kwargs) -> Response:
        response: Response = self.__session.delete(url=url, **kwargs)
        self.__raise_if_disconnected(response=response)
        return response
