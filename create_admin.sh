#!/bin/bash
# Script to create default admin user
cd "$(dirname "$0")"
source venv/bin/activate 2>/dev/null || true
python -m app.core.seed
