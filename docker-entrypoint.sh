#!/bin/bash

set -e

# Function to run migrations
run_migrations() {
    echo "Running migrations..."
    python listings/manage.py migrate
}

# Function to run linting checks
run_lint() {
    echo "Running linting checks..."
    flake8 listings
    black --check listings
    isort --check-only listings
}

# Function to run type checks
run_type_check() {
    echo "Running type checks..."
    mypy listings
}

# Function to run all checks
run_all_checks() {
    echo "Running all checks..."
    run_lint
    run_type_check
}

# Check if the command is a linting command
is_lint_command() {
    case "$1" in
        "lint"|"type-check"|"format"|"check")
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Only run migrations if not running a linting command
if ! is_lint_command "$1"; then
    run_migrations
fi

case "$1" in
    "lint")
        run_lint
        exit 0
        ;;
    "type-check")
        run_type_check
        exit 0
        ;;
    "format")
        echo "Formatting code..."
        black listings
        isort listings
        exit 0
        ;;
    "check")
        run_all_checks
        exit 0
        ;;
esac

# Execute the passed command
exec "$@" 