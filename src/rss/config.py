class ProxyConfig:
    def __init__(self) -> None:
        pass


class RssSubConfig:
    def __init__(self) -> None:
        pass

    # base config
    @property
    def url(self):
        """The url property."""
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    # TODO: add proxy config
    @property
    def proxyConfig(self) -> ProxyConfig | None:
        """The proxyConfig property."""
        return self._proxyConfig

    @proxyConfig.setter
    def proxyConfig(self, value: ProxyConfig | None):
        self._proxyConfig = value

    # filter config
    @property
    def filter(self):
        """The filter property."""
        return self._filter

    @filter.setter
    def filter(self, value):
        self._filter = value

    # download config
    @property
    def downloadDir(self):
        """The downloadDir property."""
        return self._downloadDir

    @downloadDir.setter
    def downloadDir(self, value):
        self._downloadDir = value
