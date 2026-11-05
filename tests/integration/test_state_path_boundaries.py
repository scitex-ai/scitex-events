"""Caller-provided event types must not select paths outside runtime state."""

import json

import pytest

import scitex_events as events


def test_emit_rejects_parent_path_before_creating_state(tmp_path, env_save_restore):
    # Arrange
    base = tmp_path / "state"
    env_save_restore("SCITEX_DIR", str(base))
    env_save_restore("SCITEX_API_KEY", "")
    rejected = False
    # Act
    try:
        events.emit("../outside", project="owned-fixture")
    except ValueError:
        rejected = True
    # Assert
    assert (rejected, base.exists()) == (True, False)


def test_latest_cannot_read_parent_file(tmp_path, env_save_restore):
    # Arrange
    from scitex_config._ecosystem import local_state

    env_save_restore("SCITEX_DIR", str(tmp_path))
    runtime = local_state.runtime_path("events")
    runtime.mkdir(parents=True, exist_ok=True)
    outside = runtime.parent / "owned-secret_latest.json"
    original = json.dumps({"owned_fixture": "must not be returned"})
    outside.write_text(original)
    rejected = False
    # Act
    try:
        events.latest("../owned-secret")
    except ValueError:
        rejected = True
    # Assert
    assert (rejected, outside.read_text()) == (True, original)


@pytest.mark.parametrize(
    "event_type",
    ["../parent", "a/b", "a\\b", "/absolute", "C:\\file", "C:file", "", ".", "..", "bad\x00name"],
)
def test_schema_refuses_path_shaped_types_without_io(event_type):
    # Arrange
    error_type = None
    # Act
    try:
        events.Event(type=event_type, project="owned-fixture")
    except ValueError as error:
        error_type = type(error)
    # Assert
    assert error_type is ValueError


@pytest.mark.parametrize("event_type", [None, 42])
def test_schema_refuses_nonstring_types(event_type):
    # Arrange
    error_type = None
    # Act
    try:
        events.Event(type=event_type, project="owned-fixture")
    except TypeError as error:
        error_type = type(error)
    # Assert
    assert error_type is TypeError


@pytest.mark.parametrize("event_type", ["test_complete", "stage-2.result", "測定完了"])
def test_valid_identifiers_round_trip_through_real_state(
    tmp_path, env_save_restore, event_type
):
    # Arrange
    env_save_restore("SCITEX_DIR", str(tmp_path))
    env_save_restore("SCITEX_API_KEY", "")
    # Act
    event = events.emit(event_type, project="owned-fixture", payload={"rows": 3})
    last = events.latest(event_type)
    history = events.history(limit=1)
    # Assert
    assert (last, history) == (event.to_dict(), [event.to_dict()])
