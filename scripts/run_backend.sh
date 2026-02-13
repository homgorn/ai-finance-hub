#!/usr/bin/env bash
set -euo pipefail
uvicorn src.backend.app.main:app --reload --port 8000
