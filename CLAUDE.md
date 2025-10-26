# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SoundToAct is a Korean voice-triggered automation app that executes predefined actions when specific keywords are detected. The system uses OpenAI Whisper (with Google Speech API fallback) for Korean speech recognition and supports actions like making calls, playing music, and controlling lights.

**Tech Stack:**
- Backend: Python 3.13+, FastAPI, SpeechRecognition, OpenAI Whisper
- Frontend: React 19, Vite
- Package Manager: `uv` for Python, `npm` for frontend
- Optional: Idris2 for formal specifications (presentations only)

**Important:** Python dependencies managed via `uv`. To add dependencies: `uv add <package>`. Frontend dependencies via `npm install <package>`.

## Development Commands

### Backend (Python)

```bash
# Install dependencies
uv sync

# Add new dependency
uv add <package-name>

# Run API server (development with auto-reload)
uv run python main.py server --reload

# Run API server (production)
uv run python main.py server --port 8000

# Run CLI mode (direct voice interaction without web UI)
uv run python main.py cli

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=app --cov-report=html

# Run specific test file
uv run pytest tests/test_api.py

# Run specific test by name
uv run pytest -k test_name

# Test microphone setup
uv run python test_microphone.py
```

### Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Lint
npm run lint

# Preview production build
npm preview
```

### Running the Full Stack

Terminal 1 (Backend):
```bash
uv run python main.py server --reload
```

Terminal 2 (Frontend):
```bash
cd frontend && npm run dev
```

Access: http://localhost:3000 (frontend) and http://localhost:8000/docs (API docs)

## Architecture

### Core Components

**VoiceListener** (`app/voice_listener.py`):
- Manages microphone initialization and calibration
- Handles speech recognition using Whisper (primary) and Google Speech API (fallback)
- Maintains keyword-to-action mappings
- Supports both single-shot (`listen_once()`) and continuous listening (`start_listening()`)

**ActionRegistry** (`app/actions.py`):
- Central registry for all action handlers
- Default actions: `call`, `music`, `lights`
- Factory pattern: `create_action()` returns a callable that encapsulates action type and parameters

**FastAPI Server** (`app/api.py`):
- RESTful API with CORS enabled
- Key endpoints:
  - `POST /keywords` - Register keyword-action mappings
  - `POST /listen` - One-time voice recognition
  - `POST /listen/test?text=<keyword>` - Test mode without microphone
  - `GET /keywords` - List registered keywords
  - `DELETE /keywords/{keyword}` - Remove keyword
- Global `VoiceListener` instance managed via lifespan context

**Data Models** (`app/models.py`):
- Pydantic models for request/response validation
- `KeywordActionCreate`, `KeywordActionResponse`, `ListenRequest`, `ListenResponse`, `StatusResponse`

### Data Flow

1. User registers keyword via API/Web UI → stored in `VoiceListener.keyword_actions`
2. User triggers voice recognition → `listen_once()` captures audio
3. Whisper/Google recognizes text → `check_keywords()` scans for matches
4. Matching keyword → executes associated action from `ActionRegistry`
5. Action returns result → forwarded to API response

### Entry Points

- `main.py` - CLI argument parser, supports `cli` and `server` modes
- CLI mode: Direct terminal interaction with continuous listening
- Server mode: Runs uvicorn with FastAPI app for web/API access

## Adding New Actions

To add a custom action type:

1. Add handler method in `app/actions.py`:
```python
@staticmethod
def my_action(params: dict):
    """Handle custom action"""
    param = params.get("param", "default")
    message = f"✨ Custom action: {param}"
    logger.info(message)
    print(message)
    return {"status": "success", "action": "my_action", "message": message}
```

2. Register in `ActionRegistry._register_default_actions()`:
```python
self.register("my_action", self.my_action)
```

3. Use via API:
```bash
curl -X POST http://localhost:8000/keywords \
  -H "Content-Type: application/json" \
  -d '{"keyword": "custom", "action_type": "my_action", "action_params": {"param": "value"}}'
```

## Voice Recognition Details

- **Primary**: OpenAI Whisper (runs locally, 139MB model downloaded on first use)
- **Fallback**: Google Speech Recognition API (requires internet)
- **Language**: Korean (`ko-KR` / `language="korean"`)
- **Sensitivity**: Energy threshold set to 50 (very low for quiet environments)
- **Flow**: `listen_once()` → Whisper → (if fails) → Google → (if fails) → English fallback

## Presentation Generation (Optional)

The `presentations/` directory contains a formal specification workflow using Idris2 for generating PowerPoint presentations. This is a separate subsystem that demonstrates formal verification principles.

**Complete workflow:**

```bash
cd presentations

# 1. Validate Idris2 specifications (type-safe)
idris2 --check Presentation.idr
idris2 --check ImageSpec.idr

# 2. Generate JSON from specs
python3 slides_from_idris.py

# 3. Generate images
python3 generate_images_from_spec.py

# 4. Create PowerPoint
python3 create_pptx_with_images.py

# 5. Validate output
python3 validate_ppt.py
```

**Note:** This workflow generates a type-safe, validated PowerPoint presentation. Idris2 specifications ensure correctness at compile-time. Output is `output/SoundToAct_Presentation_WithImages.pptx`. See `presentations/README.md` for detailed design principles and customization options.

**Known issues:** The generated .pptx files have compatibility issues with Apple Keynote due to python-pptx limitations. See `presentations/KEYNOTE_COMPATIBILITY_ISSUES.md` for details. PowerPoint and LibreOffice Impress work correctly.

## Testing Notes

- Coverage target: 81% (current)
- Test files in `tests/` directory
- `conftest.py` contains shared fixtures
- Mock microphone in tests to avoid hardware dependency
- Key test files:
  - `test_api.py` - API endpoint tests
  - `test_voice_listener.py` - Voice recognition tests
  - `test_actions.py` - Action handler tests
  - `test_models.py` - Pydantic model validation tests

## Common Issues

**Microphone not working:**
1. Check system permissions (Privacy → Microphone)
2. Run `uv run python test_microphone.py` for diagnostics
3. Verify PortAudio installed (`brew install portaudio` on macOS)

**Whisper fails:**
- Ensure `soundfile` is installed: `uv add soundfile`
- Check Whisper model downloaded (automatic on first run)
- Fallback to Google should work automatically

**Port conflicts:**
- Backend: `--port 8080` flag
- Frontend: Edit `vite.config.js`

## Platform-Specific

- **macOS**: Requires PortAudio (`brew install portaudio`)
- **Windows**: PyAudio auto-installs, no PortAudio needed
- **Linux**: Install `portaudio19-dev` via apt

## API Endpoints Reference

- `GET /` - API info
- `GET /status` - Listener status and registered keywords
- `POST /keywords` - Register keyword
- `GET /keywords` - List keywords
- `DELETE /keywords/{keyword}` - Delete keyword
- `POST /listen` - Perform voice recognition
- `POST /listen/test?text=<keyword>` - Test without microphone
- `POST /listen/start` - Start continuous listening (placeholder)
- `POST /listen/stop` - Stop continuous listening

Full interactive API docs: http://localhost:8000/docs
