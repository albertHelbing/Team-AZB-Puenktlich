# Pünktlich.

> Wake up *just* late enough. Pünktlich looks at tomorrow's first lecture, asks the VVS how long the trip takes, and sets a chain of Android alarms so you leave the house exactly on time.

This repository is an umbrella for two GitHub projects:

- **`app/`** — the Flutter mobile app (`puenktlich`)
- **`api/`** — the FastAPI backend (`puenktlich-api`) deployed on Vercel

## Who this is for

| | |
|---|---|
| **Role** | Flutter / Python developer contributing to or self-hosting Pünktlich |
| **Skill level** | Comfortable with `flutter`, `pip`/`pipenv`, and Android tooling |
| **Context** | macOS or Linux workstation; Android device or emulator for the app |
| **Primary goal** | Get the app running on a phone, talking to either the hosted or a local API |

End users (students in the Stuttgart / VVS area) only need the published Android build — see [Basic usage](#basic-usage).

## The core idea

Pünktlich treats your morning as a backwards-scheduled chain:

```
[wake up] ──► [prep time] ──► [travel time] ──► [first lecture starts]
```

The app reads `first lecture starts` from your device calendar, subtracts your `prep time`, then asks the API for the `travel time` between two VVS stops at the required arrival time. The result is an *alarm anchor*. Because snoozing is unreliable, the app sets **N alarms one minute apart** starting at that anchor — that is the only state it persists in the OS.

Everything else is recomputed each time you press **Wecker stellen** ("Set alarm"). There is no background service, no account, no database.

## Architecture at a glance

- **Flutter app** (`app/puenktlich-main/lib/main.dart`) — single-screen Material UI, German locale only, Android-targeted (uses `android_intent_plus` to fire the system `SET_ALARM` intent).
- **FastAPI backend** (`api/puenktlich-api-main/main.py`) — two endpoints:
  - `GET /stops?inputStr=<query>` — autocomplete against the VVS stop finder
  - `GET /trips?origin=<id>&destination=<id>&year=...&minute=...` — returns trip duration in minutes for an *arrival* at the given timestamp
- **Hosted API**: `https://puenktlich-api.vercel.app` (the URL is currently hard-coded in `app/puenktlich-main/lib/main.dart`).

## Getting started

Pick the path that matches what you want to do.

### Run the app against the hosted API (fastest)

1. Install the [Flutter SDK](https://docs.flutter.dev/get-started/install) (Dart SDK ≥ 3.9.2 is bundled).
2. Plug in an Android device (USB debugging on) or start an Android emulator.
3. From the app folder, fetch packages and run:

   ```bash
   flutter pub get
   flutter run
   ```

4. On first launch, grant the **Calendar** permission when prompted. The alarm intent does not need a runtime permission.

That's it — the app talks to the production API at `puenktlich-api.vercel.app`. You can immediately follow [Set your first alarm chain](#set-your-first-alarm-chain).

### Run the API locally

Useful if you want to change endpoints or test against a different VVS region.

1. Install Python 3.11+ and create a virtual environment:

   ```bash
   cd api/puenktlich-api-main 
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Start the dev server:

   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. Smoke-test it:

   ```bash
   curl 'http://127.0.0.1:8000/stops?inputStr=Hauptbahnhof'
   ```

4. Point the app at your local instance by editing `app/puenktlich-main/lib/main.dart`:

   ```dart
   final stops_uri = Uri.parse("http://10.0.2.2:8000/stops");
   final trips_uri = Uri.parse("http://10.0.2.2:8000/trips");
   ```

   `10.0.2.2` is the Android emulator's alias for your host machine. On a physical device, use your machine's LAN IP.

## Basic usage

Each time you open the app, you do four things:

- **Start stop** — type a name, pick from the autocomplete list (e.g. *"Stuttgart Hauptbahnhof"*).
- **Destination stop** — same idea (e.g. *"Universität"*).
- **Calendar** — tap *"Kalender wählen"* and pick the calendar that holds your lectures.
- **Prep time** — tap the duration button to set how long you need between waking and leaving (default 1 h).
- **Alarm count** — drag the number picker (1–20) to choose how many one-minute alarms to chain.

Then tap **Wecker stellen** and the alarms appear in the system clock app for tomorrow morning.

## Set your first alarm chain

A fully worked example, end to end:

1. Open the app. It launches in German on the single-screen home page.
2. Tap **Starthaltestelle** and type your home stop, e.g. `Vaihingen`. Wait ~1s for the autocomplete to load and select the correct entry.
3. Tap **Zielhaltestelle** and type your destination stop, e.g. `Universität`. Select it.
4. Tap **Kalender wählen** ("Choose calendar"). On first run, accept the calendar permission. Pick the calendar that contains your lectures and tap **Accept**.
5. Tap the duration button below *"Ich brauche morgens"* and set your prep time, e.g. `01:00`.
6. Drag the number picker to `3` to set three alarms one minute apart.
7. Tap **Wecker stellen**. The app:
   - finds the earliest event in the selected calendar between 00:00 and 23:59 *tomorrow*,
   - asks the API how long the trip from start to destination takes if you need to arrive by that event's start time,
   - subtracts trip duration + prep time from the event start, and
   - fires three `SET_ALARM` intents at one-minute intervals starting at the result.
8. Open the system **Clock** app to confirm the alarms exist for tomorrow morning. The label of each alarm is the event title.

If nothing happens, check that:

- the selected calendar actually has an event tomorrow,
- both stops were *picked from the dropdown* (typing alone doesn't select),
- you are running on a real Android device or emulator (alarms are a no-op on iOS / desktop).

## API reference

Base URL (production): `https://puenktlich-api.vercel.app`

### `GET /stops`

| Param | Type | Description |
|---|---|---|
| `inputStr` | string | Free-text stop name. Umlauts should be ASCII-folded by the client (`ä`→`ae`, etc.) — the app does this automatically. |

Returns an array of stops. Example:

```bash
curl 'https://puenktlich-api.vercel.app/stops?inputStr=Vaihingen'
```

```json
[
  {
    "name": "Vaihingen",
    "coord": "9.115,48.728",
    "parent": "Stuttgart",
    "matchQuality": 950,
    "stopId": "5000109"
  }
]
```

### `GET /trips`

| Param | Type | Description |
|---|---|---|
| `origin` | int | `stopId` from `/stops` |
| `destination` | int | `stopId` from `/stops` |
| `year`, `month`, `day`, `hour`, `minute` | int | Desired *arrival* time |

Returns trip duration in **minutes** as a bare integer (or `null` if no connection was found).

```bash
curl 'https://puenktlich-api.vercel.app/trips?origin=5006122&destination=5006171&year=2026&month=5&day=8&hour=10&minute=0'
```

```
50
```

## Development

### App

```bash
cd app/puenktlich-main
flutter pub get
flutter analyze        # static analysis
dart format .          # formatter (CI runs --set-exit-if-changed)
flutter test           # widget tests
flutter run            # launch on a connected device
```

### API

```bash
cd api/puenktlich-api-main
pip install -r requirements.txt
pip install pytest ruff
ruff check .           # lint (CI gate)
pytest                 # unit tests in tests/test_main.py
uvicorn main:app --reload
```

CI runs Ruff + Prettier on the API repo and `dart format` + `flutter analyze` on the app repo on every push and PR to `main`.

## Deployment

- **API**: pushed to `main` is auto-deployed to Vercel via the `deploy-vercel` job in `.github/workflows/ci.yml` (requires `VERCEL_TOKEN`, `VERCEL_ORG_ID`, `VERCEL_PROJECT_ID` repo secrets).
- **App**: built locally with `flutter build apk --release` and side-loaded.

## Limitations and known gaps

- **Android only.** `setAlarm` returns immediately on non-Android platforms.
- **VVS only.** The backend is bound to the Stuttgart VVS network via [`vvspy`](https://github.com/Ari510/vvspy).
- **German UI only** (`supportedLocales: const [Locale('de')]`).
- **Coordinates are not parsed** in the app's `Stop.fromJson` (`lat`/`lng` stay `null`) — see the `TODO` in `app/puenktlich-main/lib/main.dart`.
- The **API base URL is hard-coded** in the app; changing it requires editing `main.dart`.
- The `/trips` endpoint always uses the **second-to-last trip group** the upstream returns (`trips[-2]`), which is a placeholder until per-connection selection is built.

## Maintainers

- Albert Helbing
- Ari Said
- Bojan Arnaut
- Luca Oettel
- Robin Mevissen
- Zein Delic

## Further resources

- Flutter docs: <https://docs.flutter.dev/>
- FastAPI docs: <https://fastapi.tiangolo.com/>
- VVS open data: <https://www.vvs.de/tickets-fahrkarten/services/open-data/>
- `vvspy` (the upstream Python wrapper used by the API): <https://github.com/Ari510/vvspy>
- Android `SET_ALARM` intent: <https://developer.android.com/reference/android/provider/AlarmClock#ACTION_SET_ALARM>
