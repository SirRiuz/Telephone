#!/bin/bash
set -e

# Remove previous files and folders
rm -rf aws_lambda_artifact.zip dependencies
mkdir -p dependencies

# Install dependencies into the 'dependencies' folder
pip3 install -r requirements.txt \
  --platform manylinux2014_x86_64 \
  --only-binary=:all: \
  --python-version 3.12 \
  --target=dependencies \
  --root-user-action=ignore \
  --no-cache-dir \
  --no-compile \

# limpieza rápida
find dependencies -type d \( -name tests -o -name "__pycache__" \) -prune -exec rm -rf {} +
find dependencies -type f -name "*.pyc" -delete

find core -type d \( -name tests -o -name "__pycache__" \) -prune -exec rm -rf {} +
find core -type f -name "*.pyc" -delete

find modules -type d \( -name tests -o -name "__pycache__" \) -prune -exec rm -rf {} +
find modules -type f -name "*.pyc" -delete

command -v strip >/dev/null && find dependencies -type f -name "*.so" -exec strip --strip-unneeded {} + || true

# Compress the dependencies
cd dependencies
zip -r ../aws_lambda_artifact.zip .
cd ..

# Compress all code, ignoring files defined in .cpileignore
zip -r aws_lambda_artifact.zip . -x@.cpileignore

# Clean up the temporary folder
rm -rf dependencies

echo "✅ File aws_lambda_artifact.zip generated successfully"
