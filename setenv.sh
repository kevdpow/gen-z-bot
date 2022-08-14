#!/usr/bin/env bash

# Show env vars
# grep -v '^#' .env.local

# Export env vars
export $(grep -v '^#' .env.local | xargs)