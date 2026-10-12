"""Helpers for parsing network endpoint values returned by the login service."""

from __future__ import annotations

from urllib.parse import urlsplit


def parse_host_port(endpoint: str) -> tuple[str, int]:
    """Return ``(host, port)`` from a host:port endpoint.

    The login service normally returns ``host:port`` but may return an IPv6
    address or a URL. Splitting on every colon causes the TCP worker to crash
    with ``too many values to unpack``; this parser treats the final component
    as the port and validates the result before it reaches the socket layer.
    """
    value = str(endpoint).strip()
    if not value:
        raise ValueError("endpoint is empty")

    if "://" in value:
        parsed = urlsplit(value)
        host = parsed.hostname
        port = parsed.port
        if not host or port is None:
            raise ValueError(f"endpoint must include host and port: {endpoint!r}")
    elif value.startswith("["):
        closing_bracket = value.find("]")
        if closing_bracket < 0 or closing_bracket + 1 >= len(value) or value[closing_bracket + 1] != ":":
            raise ValueError(f"endpoint must use [ipv6]:port format: {endpoint!r}")
        host = value[1:closing_bracket]
        port_text = value[closing_bracket + 2:]
        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError(f"invalid endpoint port: {endpoint!r}") from exc
    else:
        host, separator, port_text = value.rpartition(":")
        if not separator or not host or not port_text:
            raise ValueError(f"endpoint must include host and port: {endpoint!r}")
        try:
            port = int(port_text)
        except ValueError as exc:
            raise ValueError(f"invalid endpoint port: {endpoint!r}") from exc

    if not 1 <= port <= 65535:
        raise ValueError(f"endpoint port out of range: {port}")
    return host, port
