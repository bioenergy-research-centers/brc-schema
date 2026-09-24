"""NCBI Taxonomy name and label lookups through oaklib.

Lookups go to OLS (``ols:ncbitaxon``) by default, so no local copy of
NCBITaxon is needed. OLS does not report synonym types, so a name that is
only a broad synonym (such as an acronym) cannot be told apart from an exact
one; callers should screen out acronyms before calling :func:`search_name`.

Lookups can be switched off (for offline runs and tests) with
:func:`configure`. When lookups are off or OLS cannot be reached, both
functions return ``None``, meaning "unknown", which callers must keep
distinct from an empty result.
"""

import logging

logger = logging.getLogger(__name__)

DEFAULT_ADAPTER = "ols:ncbitaxon"
MAX_ATTEMPTS = 3
# After this many lookups in a row fail, the service is treated as down and
# lookups stop for the rest of the run.
MAX_CONSECUTIVE_FAILURES = 3

_settings = {"enabled": True, "adapter": DEFAULT_ADAPTER}
_state = {"adapter": None, "failed": False, "consecutive_failures": 0}
# Successful results only; a failed lookup is not cached, so it can be
# retried while the service is still considered up.
_cache = {}


def configure(enabled=True, adapter=None):
    """Turn lookups on or off and choose the oaklib adapter selector."""
    _settings["enabled"] = enabled
    _settings["adapter"] = adapter or DEFAULT_ADAPTER
    _state["adapter"] = None
    _state["failed"] = False
    _state["consecutive_failures"] = 0
    _cache.clear()


def is_enabled():
    return _settings["enabled"] and not _state["failed"]


def _get_adapter():
    if _state["adapter"] is None:
        try:
            from oaklib import get_adapter

            _state["adapter"] = get_adapter(_settings["adapter"])
        except Exception as e:  # noqa: BLE001 - any failure disables lookups
            logger.warning(
                "Taxonomy lookups disabled: could not load %s (%s)", _settings["adapter"], e
            )
            _state["failed"] = True
            return None
    return _state["adapter"]


def _with_retries(func, description):
    last_error = None
    for _ in range(MAX_ATTEMPTS):
        try:
            result = func()
        except Exception as e:  # noqa: BLE001 - network errors vary by adapter
            last_error = e
            continue
        _state["consecutive_failures"] = 0
        return result
    logger.warning("Taxonomy lookup failed for %s after %d attempts: %s",
                   description, MAX_ATTEMPTS, last_error)
    _state["consecutive_failures"] += 1
    if _state["consecutive_failures"] >= MAX_CONSECUTIVE_FAILURES:
        logger.warning(
            "Taxonomy lookups disabled for this run after %d consecutive failures",
            _state["consecutive_failures"],
        )
        _state["failed"] = True
    return None


def _cached(key, func):
    """Return a cached result, or run ``func`` through the adapter and cache it.

    ``func`` takes the adapter. Results found earlier stay usable after
    lookups are switched off; failures (``None``) are never cached.
    """
    if key in _cache:
        return _cache[key]
    if not is_enabled():
        return None
    adapter = _get_adapter()
    if adapter is None:
        return None
    result = func(adapter)
    if result is not None:
        _cache[key] = result
    return result


def search_name(name):
    """Find NCBI taxa whose label or synonym is exactly ``name``.

    Matching is case-insensitive. Returns a tuple of ``(taxid, label)``
    pairs, an empty tuple when nothing matches, or ``None`` when the lookup
    could not be made.
    """
    def lookup(adapter):
        from oaklib.datamodels.search import SearchConfiguration
        from oaklib.datamodels.search_datamodel import SearchProperty

        config = SearchConfiguration(
            properties=[SearchProperty.LABEL, SearchProperty.ALIAS], is_complete=True
        )

        def run():
            results = []
            for curie in adapter.basic_search(name, config=config):
                prefix, _, local_id = str(curie).partition(":")
                if prefix == "NCBITaxon" and local_id.isdigit():
                    results.append((int(local_id), adapter.label(curie)))
            return tuple(results)

        return _with_retries(run, repr(name))

    return _cached(("name", name), lookup)


def label_for_taxid(taxid):
    """Return the NCBI scientific name for ``taxid``, or ``None``."""
    curie = f"NCBITaxon:{int(taxid)}"
    return _cached(("label", curie), lambda adapter: _with_retries(lambda: adapter.label(curie), curie))
