import prometheus_client


class Metrics:
    def __init__(self):
        self.registry = prometheus_client.CollectorRegistry()

        self._video_processed = prometheus_client.Counter(
            "video_precessed",
            "Video processed count",
            labelnames=(),
            namespace="youtube",
            subsystem="video",
            unit="",
            registry=self.registry,
            labelvalues=None,
        )
        self._emails_found = prometheus_client.Counter(
            "emails_found",
            "Emails found",
            labelnames=(),
            namespace="youtube",
            subsystem="video",
            unit="",
            registry=self.registry,
            labelvalues=None,
        )
        self._unique_emails_found = prometheus_client.Counter(
            "unique_emails_found",
            "Unique emails found",
            labelnames=(),
            namespace="youtube",
            subsystem="video",
            unit="",
            registry=self.registry,
            labelvalues=None,
        )

    def start_server(self):
        prometheus_client.start_http_server(port=8000, registry=self.registry)

    @property
    def video_processed(self) -> prometheus_client.Counter:
        return self._video_processed

    @property
    def emails_found(self) -> prometheus_client.Counter:
        return self._emails_found

    @property
    def unique_emails_found(self) -> prometheus_client.Counter:
        return self._unique_emails_found
