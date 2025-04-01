#!/bin/bash

set -euxo pipefail

flask db init || true
flask db migrate || true
flask db upgrade || true
opentelemetry-instrument python app.py
