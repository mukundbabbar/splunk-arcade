#!/bin/bash

set -euxo pipefail

opentelemetry-instrument python app.py