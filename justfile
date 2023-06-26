project := "sync-camera-disk"

default: lint test

test: pytest

# Run pytest
pytest:
    pytest -vv --cov=sync_camera_disk --cov-report=html --cov-branch --cov-context=test

# Run all linting actions
lint: ruff mypy black

# Lint code with ruff
ruff COMMAND="check" *ARGS=".":
    poetry run ruff {{COMMAND}} {{ARGS}}

# Check code with Mypy
mypy *ARGS=".":
    poetry run mypy {{ARGS}}

# Check files with black
black *ARGS=".":
    poetry run black {{ARGS}}

# Add a CHANGELOG.md entry, e.g. just changelog-add added "My entry"
changelog-add TYPE ENTRY:
    changelog-manager add {{TYPE}} "{{ENTRY}}"

# Find out what your next released version might be based on the changelog.
next-version:
    changelog-manager suggest

# Build and create files for a release
prepare-release:
    #!/bin/bash
    set -xeuo pipefail
    changelog-manager release
    poetry version $(changelog-manager current)
    rm -rvf dist
    poetry build

# Tag and release files, make sure you run 'just prepare-release' first.
do-release:
    #!/bin/bash
    set -xeuo pipefail
    VERSION=$(changelog-manager current)
    POETRY_VERSION=$(poetry version -s)
    if [ "${VERSION}" != "${POETRY_VERSION}" ]; then
        echo "Mismatch between changelog version ${VERSION} and poetry version ${VERSION}"
        exit 1
    fi
    git add pyproject.toml CHANGELOG.md
    mkdir -p build
    changelog-manager display --version $VERSION > build/release-notes.md
    if [ ! -f dist/{{project}}-${VERSION}.tar.gz ]; then
        echo "Missing expected file in dist, did you run 'just prepare-release'?"
        exit 1
    fi
    poetry publish --dry-run
    git commit -m"Release ${VERSION}"
    git tag $VERSION
    git push origin $VERSION
    git push origin main
    gh release create $VERSION --title $VERSION -F build/release-notes.md ./dist/*
    poetry publish
    rm -rvf ./dist