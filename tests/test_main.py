from datetime import datetime
from pathlib import Path
import sys
import types

import requests
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


if "vvspy" not in sys.modules:
    vvspy_stub = types.ModuleType("vvspy")
    vvspy_stub.get_trips = lambda *args, **kwargs: []
    sys.modules["vvspy"] = vvspy_stub

import main


client = TestClient(main.app)


def test_get_stops_filters_and_maps(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {
                "locations": [
                    {
                        "type": "stop",
                        "name": "Stuttgart Hbf",
                        "coord": "9.182,48.783",
                        "parent": {"name": "Stuttgart"},
                        "matchQuality": 100,
                        "properties": {"stopId": "5000001"},
                    },
                    {
                        "type": "poi",
                        "name": "Ignore Me",
                    },
                ]
            }

    def fake_get(url, params, timeout):
        assert url == main.BASE_URL
        assert params["name_sf"] == "Hbf"
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr(main.requests, "get", fake_get)

    response = client.get("/stops", params={"inputStr": "Hbf"})

    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "Stuttgart Hbf",
            "coord": "9.182,48.783",
            "parent": "Stuttgart",
            "matchQuality": 100,
            "stopId": "5000001",
        }
    ]


def test_get_stops_returns_empty_list_when_no_stop_locations(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"locations": [{"type": "poi", "name": "Museum"}]}

    monkeypatch.setattr(main.requests, "get", lambda *args, **kwargs: FakeResponse())

    response = client.get("/stops", params={"inputStr": "Museum"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_stops_returns_empty_list_when_locations_key_missing(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return {"meta": {"ok": True}}

    monkeypatch.setattr(main.requests, "get", lambda *args, **kwargs: FakeResponse())

    response = client.get("/stops", params={"inputStr": "Anything"})

    assert response.status_code == 200
    assert response.json() == []


def test_get_stops_translates_request_exception_to_502(monkeypatch):
    def fake_get(*args, **kwargs):
        raise requests.RequestException("network failure")

    monkeypatch.setattr(main.requests, "get", fake_get)

    response = client.get("/stops", params={"inputStr": "Hbf"})

    assert response.status_code == 502
    assert "Upstream error" in response.json()["detail"]


def test_trips_returns_duration_minutes(monkeypatch):
    class Endpoint:
        def __init__(self, dep=None, arr=None):
            self.departure_time_estimated = dep
            self.arrival_time_estimated = arr

    class Connection:
        def __init__(self, departure, arrival):
            self.origin = Endpoint(dep=departure)
            self.destination = Endpoint(arr=arrival)

    class TripGroup:
        def __init__(self, connections):
            self.connections = connections

    def fake_get_trips(origin, destination, arrival_time, **params):
        assert origin == 5006122
        assert destination == 5006171
        assert arrival_time == datetime(2026, 4, 10, 10, 0)
        assert params == {
            "itdDateTimeDepArr": "arr",
            "itdTripDateTimeDepArr": "arr",
        }
        return [
            TripGroup([]),
            TripGroup(
                [
                    Connection(datetime(2026, 4, 10, 9, 10), datetime(2026, 4, 10, 9, 30)),
                    Connection(datetime(2026, 4, 10, 9, 35), datetime(2026, 4, 10, 10, 0)),
                ]
            ),
            TripGroup([]),
        ]

    monkeypatch.setattr(main.vvspy, "get_trips", fake_get_trips)

    response = client.get(
        "/trips",
        params={
            "origin": 5006122,
            "destination": 5006171,
            "year": 2026,
            "month": 4,
            "day": 10,
            "hour": 10,
            "minute": 0,
        },
    )

    assert response.status_code == 200
    assert response.json() == 50


def test_trips_translates_request_exception_to_502(monkeypatch):
    def fake_get_trips(*args, **kwargs):
        raise requests.RequestException("upstream timeout")

    monkeypatch.setattr(main.vvspy, "get_trips", fake_get_trips)

    response = client.get(
        "/trips",
        params={
            "origin": 1,
            "destination": 2,
            "year": 2026,
            "month": 4,
            "day": 10,
            "hour": 10,
            "minute": 0,
        },
    )

    assert response.status_code == 502
    assert "Upstream error" in response.json()["detail"]


def test_trips_returns_null_when_vvspy_returns_no_trips(monkeypatch):
    monkeypatch.setattr(main.vvspy, "get_trips", lambda *args, **kwargs: [])

    response = client.get(
        "/trips",
        params={
            "origin": 1,
            "destination": 2,
            "year": 2026,
            "month": 4,
            "day": 10,
            "hour": 10,
            "minute": 0,
        },
    )

    assert response.status_code == 200
    assert response.json() is None


def test_test_endpoint_returns_vvspy_result(monkeypatch):
    expected = [{"ok": True}]

    def fake_get_trips(origin, destination):
        assert origin == 5006122
        assert destination == 5006171
        return expected

    monkeypatch.setattr(main.vvspy, "get_trips", fake_get_trips)

    response = client.get("/test")

    assert response.status_code == 200
    assert response.json() == expected
