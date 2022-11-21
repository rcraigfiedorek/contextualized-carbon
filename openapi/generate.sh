#!/bin/bash

OPENAPI_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
PROJECT_DIR="$(dirname "$OPENAPI_DIR")"

source "$PROJECT_DIR/server/.venv/bin/activate"
export FLASK_APP="$PROJECT_DIR/server/api"
flask spec -o "$OPENAPI_DIR/openapi.json"

docker run --rm -v "$OPENAPI_DIR:/local" openapitools/openapi-generator-cli:latest generate \
    -i "/local/openapi.json" \
    -g typescript-axios \
    -o /local/out/ts

cp -a "$OPENAPI_DIR/out/ts/." "$PROJECT_DIR/client/src/api"
