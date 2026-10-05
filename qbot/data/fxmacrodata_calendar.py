"""FXMacroData client and pandas helpers for macro, FX, and event data."""

from __future__ import annotations

import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd

FXMACRODATA_BASE_URL = "https://api.fxmacrodata.com/v1"
FXMACRODATA_API_KEY_ENV_VARS = ("FXMACRODATA_API_KEY", "FXMD_API_KEY")
# List endpoints return at most 100 rows per request, newest first.
FXMACRODATA_PAGE_SIZE = 100
FXMACRODATA_MAX_PAGES = 100
FXMACRODATA_PAGED_DATASETS = {
    "announcements",
    "predictions",
    "forex",
    "cot",
    "commodity",
    "rate_differentials",
    "forward_differentials",
    "risk_sentiment",
}
FXMACRODATA_ENDPOINTS = {
    "data_catalogue": (
        "data_catalogue/{currency}",
        {"include_capabilities", "include_coverage", "indicator"},
    ),
    "announcements": (
        "announcements/{currency}/{indicator}",
        {
            "start_date",
            "end_date",
            "series_mode",
            "limit",
            "offset",
            "page",
            "seasonality",
            "frequency",
            "revisions",
            "basis",
            "official_only",
        },
    ),
    "latest_announcements": ("announcements/{currency}/latest", set()),
    "announcement_changes": (
        "announcements/changes",
        {"currencies", "indicators", "since", "limit", "payload"},
    ),
    "predictions": (
        "predictions/{currency}/{indicator}",
        {
            "prediction_type",
            "prediction_source",
            "start_date",
            "end_date",
            "limit",
            "offset",
            "page",
        },
    ),
    "calendar": (
        "calendar/{currency}",
        {"indicator", "start_date", "end_date", "timezone"},
    ),
    "forex": (
        "forex/{base}/{quote}",
        {"start_date", "end_date", "limit", "offset", "page", "indicators"},
    ),
    "cot": ("cot/{currency}", {"start_date", "end_date", "limit", "offset", "page"}),
    "commodity": (
        "commodities/{indicator}",
        {"start_date", "end_date", "limit", "offset", "page"},
    ),
    "commodities_latest": ("commodities/latest", set()),
    "curves": ("curves/{currency}", {"curve_family", "metric", "date"}),
    "curve_proxies": ("curve_proxies/{currency}", {"curve_family", "date"}),
    "forward_curves": ("forward_curves/{currency}", {"curve_family", "method", "date"}),
    "rate_differentials": (
        "rate_differentials/{base}/{quote}",
        {"measure", "start_date", "end_date", "limit", "offset"},
    ),
    "forward_differentials": (
        "forward_differentials/{base}/{quote}",
        {
            "curve_family",
            "start_tenor_years",
            "end_tenor_years",
            "start_date",
            "end_date",
            "limit",
            "offset",
        },
    ),
    "market_sessions": ("market_sessions", {"at"}),
    "risk_sentiment": ("risk_sentiment", {"start_date", "end_date", "limit", "offset"}),
    "news": ("news/{currency}", {"limit", "offset"}),
    "press_releases": ("press-releases/{currency}", {"limit", "offset"}),
}
FXMACRODATA_DATASET_ALIASES = {
    "catalogue": "data_catalogue",
    "macro": "announcements",
    "macro_indicators": "announcements",
    "release_calendar": "calendar",
    "calendar": "calendar",
    "changes": "announcement_changes",
    "latest": "latest_announcements",
    "fx": "forex",
    "fx_spot": "forex",
    "commodities": "commodity",
    "press-releases": "press_releases",
}


def _env_api_key():
    for name in FXMACRODATA_API_KEY_ENV_VARS:
        value = os.environ.get(name)
        if value:
            return value
    return None


def _dataset_name(dataset):
    normalized = dataset.lower().replace("-", "_")
    return FXMACRODATA_DATASET_ALIASES.get(normalized, normalized)


def _clean_params(params):
    cleaned = {}
    for key, value in (params or {}).items():
        if value is None:
            continue
        if isinstance(value, (list, tuple, set)):
            value = ",".join(str(item) for item in value)
        cleaned[key] = value
    return cleaned


def _format_path(path_template, kwargs):
    values = {
        key: str(kwargs[key]).lower()
        for key in ("currency", "base", "quote")
        if key in kwargs
    }
    if "indicator" in kwargs:
        values["indicator"] = str(kwargs["indicator"])
    try:
        return path_template.format(**values)
    except KeyError as exc:
        raise ValueError(
            "missing required FXMacroData parameter: %s" % exc.args[0]
        ) from exc


def _payload_rows(payload):
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        return []
    data = payload.get("data")
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        rows = []
        for key, value in sorted(data.items()):
            if isinstance(value, dict):
                row = {"indicator": key}
                row.update(value)
            else:
                row = {"indicator": key, "value": value}
            rows.append(row)
        return rows
    for key in ("events", "results", "items", "rows"):
        value = payload.get(key)
        if isinstance(value, list):
            return value
    return [payload]


def _frame_from_payload(payload, limit=None, index=True):
    frame = pd.DataFrame(_payload_rows(payload))
    if frame.empty:
        return frame
    for column in ("date", "timestamp", "release_date"):
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")
    for column in ("announcement_datetime", "announcement_datetime_utc", "time"):
        if column not in frame.columns:
            continue
        if pd.api.types.is_numeric_dtype(frame[column]):
            frame[column] = pd.to_datetime(
                frame[column], unit="s", utc=True, errors="coerce"
            )
        else:
            frame[column] = pd.to_datetime(frame[column], utc=True, errors="coerce")
    if index:
        for column in ("date", "timestamp", "release_date", "time"):
            if column in frame.columns:
                frame = frame.dropna(subset=[column]).set_index(column).sort_index()
                break
    if limit is not None:
        frame = frame.head(max(1, int(limit)))
    return frame


def _checked_payload(payload):
    """Reject error bodies and non-JSON-object/array payloads with a clean error."""
    if isinstance(payload, dict) and "detail" in payload and "data" not in payload:
        raise ValueError(
            "FXMacroData returned an error response: %s" % payload["detail"]
        )
    if not isinstance(payload, (dict, list)):
        raise ValueError("FXMacroData returned an unexpected response")
    return payload


def _filter_market_tier(frame, min_tier):
    if min_tier is None or frame.empty or "market_tier" not in frame.columns:
        return frame
    tier = pd.to_numeric(frame["market_tier"], errors="coerce").fillna(99)
    return frame.loc[tier <= int(min_tier)]


class FXMacroDataClient:
    """Small client for the public FXMacroData read/data API surface."""

    def __init__(self, api_key=None, base_url=FXMACRODATA_BASE_URL, timeout=30):
        self.api_key = (api_key or _env_api_key() or "").strip() or None
        if self.api_key and not self.api_key.isprintable():
            raise ValueError("FXMacroData API key contains invalid characters")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, url, **kwargs):
        headers = {
            "User-Agent": "fxmacrodata-integration",
            **kwargs.pop("headers", {}),
        }
        request = Request(url, headers=headers, **kwargs)
        if self.api_key:
            # Unredirected: the key is never re-sent if the API answers with a redirect.
            request.add_unredirected_header("X-API-Key", self.api_key)
        return request

    def _open_json(self, request):
        with urlopen(request, timeout=self.timeout) as response:  # nosec B310
            return _checked_payload(json.loads(response.read().decode("utf-8")))

    def fetch_dataset(self, dataset, **kwargs):
        dataset = _dataset_name(dataset)
        if dataset not in FXMACRODATA_ENDPOINTS:
            raise ValueError(
                "dataset must be one of %s" % ", ".join(sorted(FXMACRODATA_ENDPOINTS))
            )
        path_template, query_keys = FXMACRODATA_ENDPOINTS[dataset]
        path = _format_path(path_template, kwargs)
        query = _clean_params({key: kwargs.get(key) for key in query_keys})
        if dataset in FXMACRODATA_PAGED_DATASETS and "limit" in query:
            query["limit"] = min(int(query["limit"]), FXMACRODATA_PAGE_SIZE)
        url = "%s/%s" % (self.base_url, path.lstrip("/"))
        if query:
            url = "%s?%s" % (url, urlencode(query))
        return self._open_json(self._request(url))

    def graphql(self, query, variables=None):
        body = json.dumps({"query": query, "variables": variables or {}}).encode(
            "utf-8"
        )
        request = self._request(
            "%s/graphql" % self.base_url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return self._open_json(request)

    def to_dataframe(self, payload, limit=None, index=True):
        return _frame_from_payload(payload, limit=limit, index=index)

    def data_catalogue(self, currency="usd", **kwargs):
        return self.fetch_dataset("data_catalogue", currency=currency, **kwargs)

    def announcements(self, currency, indicator, **kwargs):
        return self.fetch_dataset(
            "announcements", currency=currency, indicator=indicator, **kwargs
        )

    macro_indicators = announcements

    def latest_announcements(self, currency="usd"):
        return self.fetch_dataset("latest_announcements", currency=currency)

    def announcement_changes(self, **kwargs):
        return self.fetch_dataset("announcement_changes", **kwargs)

    def predictions(self, currency, indicator, **kwargs):
        return self.fetch_dataset(
            "predictions", currency=currency, indicator=indicator, **kwargs
        )

    def release_calendar(self, currency="usd", **kwargs):
        return self.fetch_dataset("calendar", currency=currency, **kwargs)

    def forex(self, base, quote, **kwargs):
        return self.fetch_dataset("forex", base=base, quote=quote, **kwargs)

    def cot(self, currency, **kwargs):
        return self.fetch_dataset("cot", currency=currency, **kwargs)

    def commodity(self, indicator, **kwargs):
        return self.fetch_dataset("commodity", indicator=indicator, **kwargs)

    commodities = commodity

    def commodities_latest(self):
        return self.fetch_dataset("commodities_latest")

    def curves(self, currency, **kwargs):
        return self.fetch_dataset("curves", currency=currency, **kwargs)

    def curve_proxies(self, currency, **kwargs):
        return self.fetch_dataset("curve_proxies", currency=currency, **kwargs)

    def forward_curves(self, currency, **kwargs):
        return self.fetch_dataset("forward_curves", currency=currency, **kwargs)

    def rate_differentials(self, base, quote, **kwargs):
        return self.fetch_dataset(
            "rate_differentials", base=base, quote=quote, **kwargs
        )

    def forward_differentials(self, base, quote, **kwargs):
        return self.fetch_dataset(
            "forward_differentials", base=base, quote=quote, **kwargs
        )

    def market_sessions(self, **kwargs):
        return self.fetch_dataset("market_sessions", **kwargs)

    def risk_sentiment(self, **kwargs):
        return self.fetch_dataset("risk_sentiment", **kwargs)

    def news(self, currency, **kwargs):
        return self.fetch_dataset("news", currency=currency, **kwargs)

    def press_releases(self, currency, **kwargs):
        return self.fetch_dataset("press_releases", currency=currency, **kwargs)

    def fetch_rows(
        self, dataset, limit=None, max_pages=FXMACRODATA_MAX_PAGES, **kwargs
    ):
        """Page through a list endpoint and return up to ``limit`` rows.

        Rows come back newest first, at most 100 per request, so the window is
        read with ``offset`` until ``pagination.has_more`` is false. With
        ``limit=None`` the whole window is read, up to ``max_pages`` requests.
        """
        kwargs.pop("page", None)
        offset = int(kwargs.pop("offset", None) or 0)
        limit = None if limit is None else max(1, int(limit))
        rows = []
        for _ in range(max(1, int(max_pages))):
            page_size = FXMACRODATA_PAGE_SIZE
            if limit is not None:
                page_size = min(page_size, limit - len(rows))
            payload = self.fetch_dataset(
                dataset, limit=page_size, offset=offset, **kwargs
            )
            page = payload.get("data") if isinstance(payload, dict) else payload
            if not isinstance(page, list) or not page:
                break
            rows.extend(page)
            if limit is not None and len(rows) >= limit:
                break
            pagination = (
                payload.get("pagination") if isinstance(payload, dict) else None
            )
            if not isinstance(pagination, dict) or not pagination.get("has_more"):
                break
            next_offset = pagination.get("next_offset")
            offset = int(next_offset) if next_offset is not None else offset + len(page)
        return rows

    def dataframe(self, dataset, limit=None, min_tier=None, index=True, **kwargs):
        name = _dataset_name(dataset)
        if name in FXMACRODATA_PAGED_DATASETS:
            payload = {"data": self.fetch_rows(name, limit=limit, **kwargs)}
        else:
            api_limit = None if name == "calendar" else limit
            payload = self.fetch_dataset(
                name, **{**kwargs, **({"limit": api_limit} if api_limit else {})}
            )
        frame = self.to_dataframe(payload, limit=limit, index=index)
        return _filter_market_tier(frame, min_tier)


def load_fxmacrodata_dataset(
    dataset, api_key=None, base_url=FXMACRODATA_BASE_URL, timeout=30, **kwargs
):
    """Load any public FXMacroData read dataset into a pandas DataFrame."""
    return FXMacroDataClient(
        api_key=api_key, base_url=base_url, timeout=timeout
    ).dataframe(dataset, **kwargs)


def get_fxmacrodata_dataset(*args, **kwargs):
    return load_fxmacrodata_dataset(*args, **kwargs)


def load_fxmacrodata_catalogue(
    currency="usd",
    include_capabilities=False,
    include_coverage=False,
    indicator=None,
    **kwargs,
):
    return load_fxmacrodata_dataset(
        "data_catalogue",
        currency=currency,
        include_capabilities=include_capabilities,
        include_coverage=include_coverage,
        indicator=indicator,
        **kwargs,
    )


def load_fxmacrodata_announcements(
    currency, indicator, start_date=None, end_date=None, limit=20, **kwargs
):
    return load_fxmacrodata_dataset(
        "announcements",
        currency=currency,
        indicator=indicator,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        **kwargs,
    )


def load_fxmacrodata_latest_announcements(currency="usd", **kwargs):
    return load_fxmacrodata_dataset("latest_announcements", currency=currency, **kwargs)


def load_fxmacrodata_announcement_changes(
    currencies=None, indicators=None, since=None, limit=100, **kwargs
):
    return load_fxmacrodata_dataset(
        "announcement_changes",
        currencies=currencies,
        indicators=indicators,
        since=since,
        payload=kwargs.pop("payload", "compact"),
        limit=limit,
        **kwargs,
    )


def load_fxmacrodata_predictions(
    currency, indicator, start_date=None, end_date=None, limit=20, **kwargs
):
    return load_fxmacrodata_dataset(
        "predictions",
        currency=currency,
        indicator=indicator,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        **kwargs,
    )


def load_fxmacrodata_release_calendar(
    currency="usd",
    indicator=None,
    start_date=None,
    end_date=None,
    timezone=None,
    limit=100,
    min_tier=None,
    **kwargs,
):
    return load_fxmacrodata_dataset(
        "calendar",
        currency=currency,
        indicator=indicator,
        start_date=start_date,
        end_date=end_date,
        timezone=timezone,
        limit=limit,
        min_tier=min_tier,
        **kwargs,
    )


def load_fxmacrodata_forex(
    base, quote, start_date=None, end_date=None, limit=20, indicators=None, **kwargs
):
    return load_fxmacrodata_dataset(
        "forex",
        base=base,
        quote=quote,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        indicators=indicators,
        **kwargs,
    )


def load_fxmacrodata_cot(currency, start_date=None, end_date=None, limit=20, **kwargs):
    return load_fxmacrodata_dataset(
        "cot",
        currency=currency,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        **kwargs,
    )


def load_fxmacrodata_commodity(
    indicator, start_date=None, end_date=None, limit=20, **kwargs
):
    return load_fxmacrodata_dataset(
        "commodity",
        indicator=indicator,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        **kwargs,
    )


def load_fxmacrodata_commodities_latest(**kwargs):
    return load_fxmacrodata_dataset("commodities_latest", **kwargs)


def merge_fxmacrodata_features(left, features, tolerance="7D", direction="backward"):
    """As-of merge a price/factor frame with FXMacroData macro features."""
    if left.empty or features.empty:
        return left.copy()
    return pd.merge_asof(
        left.sort_index().copy(),
        features.sort_index().copy(),
        left_index=True,
        right_index=True,
        direction=direction,
        tolerance=pd.Timedelta(tolerance) if tolerance is not None else None,
    )


def fxmacrodata_event_windows(index, events, days_before=1, days_after=1):
    """Return a boolean Series for observations near FXMacroData release events."""
    normalized_index = pd.DatetimeIndex(index).normalize()
    mask = pd.Series(False, index=index)
    if events.empty:
        return mask
    if isinstance(events.index, pd.DatetimeIndex):
        event_dates = pd.DatetimeIndex(events.index)
    else:
        event_dates = pd.to_datetime(events.get("date"), errors="coerce")
    for event_date in pd.DatetimeIndex(event_dates).dropna().normalize():
        start = event_date - pd.Timedelta(days=days_before)
        end = event_date + pd.Timedelta(days=days_after)
        mask |= (normalized_index >= start) & (normalized_index <= end)
    return mask


get_data_catalogue = load_fxmacrodata_catalogue
get_macro_indicators = load_fxmacrodata_announcements
get_release_calendar = load_fxmacrodata_release_calendar
get_forex = load_fxmacrodata_forex
fxmacrodata_release_calendar = load_fxmacrodata_release_calendar
load_release_calendar = load_fxmacrodata_release_calendar
load_fxmacrodata_calendar = load_fxmacrodata_release_calendar
event_window_mask = fxmacrodata_event_windows
event_window_filter = fxmacrodata_event_windows
