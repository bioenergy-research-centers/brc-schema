"""Tests for failure handling and caching in taxonomy lookups."""

from brc_schema.util import taxonomy


class CountingAdapter:
    """Fails the first ``failures`` calls, then answers every name."""

    def __init__(self, failures):
        self.failures = failures
        self.calls = 0

    def basic_search(self, name, config=None):
        self.calls += 1
        if self.calls <= self.failures:
            raise ConnectionError("OLS unreachable")
        return iter(["NCBITaxon:1"])

    def label(self, curie):
        return "root"


def _use(monkeypatch, adapter):
    monkeypatch.setattr(taxonomy, "_get_adapter", lambda: adapter)
    taxonomy.configure()


def test_repeated_failures_switch_lookups_off(monkeypatch):
    adapter = CountingAdapter(failures=10**6)
    _use(monkeypatch, adapter)
    for name in ["a", "b", "c", "d", "e"]:
        assert taxonomy.search_name(name) is None
    limit = taxonomy.MAX_ATTEMPTS * taxonomy.MAX_CONSECUTIVE_FAILURES
    assert adapter.calls == limit
    assert not taxonomy.is_enabled()


def test_failed_lookup_is_not_cached(monkeypatch):
    adapter = CountingAdapter(failures=taxonomy.MAX_ATTEMPTS)
    _use(monkeypatch, adapter)
    assert taxonomy.search_name("poplar") is None
    assert taxonomy.search_name("poplar") == ((1, "root"),)


class ScriptedAdapter:
    """Each basic_search call pops the next outcome: True answers, False fails."""

    def __init__(self, outcomes):
        self.outcomes = list(outcomes)

    def basic_search(self, name, config=None):
        if not self.outcomes.pop(0):
            raise ConnectionError("OLS unreachable")
        return iter(["NCBITaxon:1"])

    def label(self, curie):
        return "root"


def test_success_resets_the_failure_count(monkeypatch):
    fail = [False] * taxonomy.MAX_ATTEMPTS
    # Two failed names, one success, two failed names: never three in a row.
    _use(monkeypatch, ScriptedAdapter(fail + fail + [True] + fail + fail))
    for name in ["a", "b", "c", "d", "e"]:
        taxonomy.search_name(name)
    assert taxonomy.is_enabled()


def test_cached_results_survive_lookups_switching_off(monkeypatch):
    adapter = CountingAdapter(failures=0)
    _use(monkeypatch, adapter)
    assert taxonomy.search_name("poplar") == ((1, "root"),)
    taxonomy._state["failed"] = True
    assert taxonomy.search_name("poplar") == ((1, "root"),)
    assert taxonomy.search_name("other") is None
