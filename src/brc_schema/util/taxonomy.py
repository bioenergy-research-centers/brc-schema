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
from functools import lru_cache

logger = logging.getLogger(__name__)

DEFAULT_ADAPTER = "ols:ncbitaxon"
MAX_ATTEMPTS = 3

_settings = {"enabled": True, "adapter": DEFAULT_ADAPTER}
_state = {"adapter": None, "failed": False}


def configure(enabled=True, adapter=None):
    """Turn lookups on or off and choose the oaklib adapter selector."""
    _settings["enabled"] = enabled
    _settings["adapter"] = adapter or DEFAULT_ADAPTER
    _state["adapter"] = None
    _state["failed"] = False
    search_name.cache_clear()
    label_for_taxid.cache_clear()


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
            return func()
        except Exception as e:  # noqa: BLE001 - network errors vary by adapter
            last_error = e
    logger.warning("Taxonomy lookup failed for %s after %d attempts: %s",
                   description, MAX_ATTEMPTS, last_error)
    return None


@lru_cache(maxsize=None)
def search_name(name):
    """Find NCBI taxa whose label or synonym is exactly ``name``.

    Matching is case-insensitive. Returns a tuple of ``(taxid, label)``
    pairs, an empty tuple when nothing matches, or ``None`` when the lookup
    could not be made.
    """
    if not is_enabled():
        return None
    adapter = _get_adapter()
    if adapter is None:
        return None

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


@lru_cache(maxsize=None)
def label_for_taxid(taxid):
    """Return the NCBI scientific name for ``taxid``, or ``None``."""
    if not is_enabled():
        return None
    adapter = _get_adapter()
    if adapter is None:
        return None
    return _with_retries(lambda: adapter.label(f"NCBITaxon:{int(taxid)}"), f"NCBITaxon:{taxid}")
