# CLAUDE.md

Guidance for working in this repository. Findings below were verified on 2026-11-09
against `master` at 973fae4 (release 1.15.0).

## What this is

`json-rpc` (PyPI) / `jsonrpc` (import name): a zero-dependency, transport-agnostic
implementation of the JSON-RPC 1.0 and 2.0 protocols, with optional Django and Flask
adapters. Users bring their own transport (HTTP, ZeroMQ, serial, raw TCP...).

Public API that users depend on — keep it backward compatible:
- `jsonrpc.JSONRPCResponseManager.handle(request_str, dispatcher, context=None)`
- `jsonrpc.Dispatcher` and the module-level `jsonrpc.dispatcher` singleton,
  `@dispatcher.add_method`, `add_method(name=..., context_arg=...)`,
  `add_object`, `add_class`, `add_dict(prefix=...)`
- `jsonrpc.exceptions.JSONRPCDispatchException(code, message, data)`
- `jsonrpc.backend.django.api.urls`, `jsonrpc.backend.flask.api.as_blueprint()`
- `JSONRPC20Request`, `JSONRPC20Response`, `JSONRPC10Request`, ... in `jsonrpc.jsonrpc1/2`

## Commands

```bash
# Run tests (Django tests need the settings module; tox sets it automatically)
DJANGO_SETTINGS_MODULE=jsonrpc.tests.test_backend_django.settings pytest -q
pip install pytest flask django   # optional backends; their tests skip if missing
tox -e py3XX                       # tox.ini is stale (pins Django 2.2 / Flask 1.1)
```

The suite (224 passed, 1 skipped) runs clean on Python 3.14 with current Django and Flask.
CircleCI config (`.circleci/config.yml`) only covers py27–py38 on deprecated images.

## Layout

| File | Role |
|---|---|
| `jsonrpc/manager.py` | `JSONRPCResponseManager`: parse → dispatch → build response. All classmethods, no instance config. |
| `jsonrpc/dispatcher.py` | `Dispatcher(MutableMapping)`: method registry + `context_arg_for_method` |
| `jsonrpc/jsonrpc.py` | `JSONRPCRequest.from_data`: picks 1.0 vs 2.0 by presence of `"jsonrpc"` key |
| `jsonrpc/jsonrpc1.py`, `jsonrpc2.py` | Request/Response models: `_data` dict + validating property setters + `.json` |
| `jsonrpc/base.py` | Shared base request/response classes |
| `jsonrpc/exceptions.py` | `JSONRPCError` (NOT an Exception) + subclasses with `CODE`/`MESSAGE`; `JSONRPCDispatchException` wraps one |
| `jsonrpc/utils.py` | `JSONSerializable`, `DatetimeDecimalEncoder`, `is_invalid_params` heuristic |
| `jsonrpc/six.py` | Vendored six (583 lines, ~30% of the package). Py2 compat only. |
| `jsonrpc/backend/{django,flask}.py` | Framework adapters + `/map` docstring view |

## Known defects (reproduced)

Fix these with a regression test each. Spec: https://www.jsonrpc.org/specification

1. **Batch with one invalid element** (`[{valid}, 1]`) returns a single `Invalid Request`;
   spec requires one error per invalid element and valid calls still executed.
   Cause: `JSONRPC20Request.from_data` raises on the first bad element.
2. **`TypeError` inside a method is misreported as Invalid params** for bound methods
   (`utils.is_invalid_params` returns True whenever `not inspect.isfunction(func)`) and for
   `*args, **kwargs` functions (issue #47). Correct approach: `inspect.signature(f).bind(...)`
   *before* calling; bind failure → -32602, anything raised afterwards → -32000.
3. **Serialization happens outside the error boundary.** The manager returns objects; `.json`
   is called later by the caller. Non-serializable results or exception args (#46) raise
   `TypeError` → HTTP 500 instead of a JSON-RPC error.
4. **`rpc.*` method names rejected in the request model** (`jsonrpc2.py` method setter), so
   OpenRPC `rpc.discover` can never be served (#119, PR #120). This is server policy and
   belongs in dispatch, not parsing.
5. **id validation**: float ids rejected (spec allows Numbers); `true`/`false` accepted because
   `bool` is an `int` subclass.
6. **`context_arg` mutates state**: writes the context into `request.params` (since
   `request.kwargs` returns the params dict itself) and sets `context["request"]` on the
   caller's dict, shared across a batch (`manager.py` `_get_responses`).
7. **JSON-RPC 1.0 responses omit `"error": null` / `"result": null`** (#113); 1.0 requires both.
8. **Exception details leak to clients**: every unhandled exception's type, args and message
   are returned in `error.data`. No way to disable or redact. Security concern.
9. `error` setters do `self._data.pop('value', None)` — typo for `'result'`
   (`jsonrpc1.py`, `jsonrpc2.py`).
10. Notifications swallow errors silently with no hook (#124); no hook to map exceptions to
    transport status, e.g. HTTP 401 (#118).
11. Backends: JSON parsed twice per request; `response.serialize` monkeypatched per instance;
    Django injects `HttpRequest` into params (forces a `request` arg on every method — the
    newer `context_arg` is the better mechanism); Flask `check_content_type` never checks
    the content type; `/map` view renders docstrings without HTML escaping; unused `time` import.
12. `jsonrpc.py` and `jsonrpc2.py` begin with a UTF-8 BOM.
13. Release hygiene: no `python_requires`; classifiers list 2.6–3.8; `setup.py` imports the
    package to read the version; git tags 1.14.0 and 1.15.0 missing (#128).

## Roadmap

Tracked publicly in https://github.com/pavlov99/json-rpc/issues/155 (pinned), with milestones
`1.15.x maintenance` (phases 0–1: #128, #133–#140, #47, #113, #46) and `2.0.0`
(phases 2–5: #141–#154, #119, #116, #59, #40, #118, #124). Reference the issue in commits/PRs
(`Fixes #N`) and tick the box in #155 when done.

## Architectural direction

Agreed principles for changes:
- **Keep**: zero runtime dependencies, transport-agnostic core, the `Dispatcher` decorator API,
  and `JSONRPCResponseManager.handle(...)` as a compatibility shim.
- **Sans-IO core**: `parse(bytes|str) -> list[Call | ErrorReply]` (never raises, per-element
  batch errors) → `dispatch` / `adispatch` (sync and async share everything except the
  invocation line) → `render(replies, serializer) -> bytes | None` (serialization inside the
  error boundary, with a safe fallback error).
- **Configurable server instance** holding registry, serializer (`dumps`/`loads` pluggable:
  json, orjson, simplejson, CBOR — #27, #94), `on_error` hook, and
  `expose_exception_details` (default False in 2.0).
- **Single exception hierarchy**: error classes are `Exception` subclasses carrying
  code/message/data, so users can `raise InvalidParams(...)` or define app errors (#40).
- **Models** become plain dataclasses; validation lives in `parse`, not property setters.
- Async lives in this package (separate module, shared core) rather than the `ajsonrpc` fork.
  Most-requested feature since 2015 (#30, #87, #116, #127, #129); previous PRs were rejected
  for copy-pasting the manager — do not repeat that.

## Python support policy

- **1.15.x**: final line for Python 2.6/2.7 and 3.x < 3.10. Bug fixes only; must stay
  py2-compatible (no f-strings, no type annotations, keep `six`).
- **2.0**: `requires-python >= 3.10`. Drop `six.py`, `is_invalid_params_py2`, `__future__`
  imports, `collections` fallbacks. Use type hints + `py.typed`, dataclasses, `pyproject.toml`,
  GitHub Actions matrix 3.10–3.14 + PyPy with current Django/Flask.
  pip honors `requires-python`, so old interpreters keep resolving to 1.15.x.

## Conventions

- Every behavior fix needs a regression test under `jsonrpc/tests/`.
- Behavior changes visible to clients (error codes, response shape, exposed data) must be
  noted in `changelog` and called out as breaking where applicable.
- Commit message prefixes used in history: `FIX:`, `REF:`, `REL:`, `ADD:`, `DOC:`.
