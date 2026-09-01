#!/bin/bash

# Phase 1: Create Enhanced Folder Structure
# This script builds out the enterprise architecture while preserving existing code

echo "📁 Creating Enhanced Folder Structure..."

# Core directories (keep existing)
mkdir -p backend/{api,services,models,utils,config,schemas}
mkdir -p dashboard/{pages,utils,static,components}
mkdir -p kafka/{producers,consumers,config}

# New enterprise directories
mkdir -p data/{historical,raw,processed,exports}
mkdir -p data/historical/{entsoe,cea,iex,kaggle}
mkdir -p analytics/{notebooks,results,models}
mkdir -p analytics/{baseline,anomaly,forecast}
mkdir -p powerbi/{dashboards,datasources,reports}
mkdir -p database/{schemas,migrations,backups}
mkdir -p docker/{postgres,kafka,config}
mkdir -p tests/{unit,integration,fixtures}
mkdir -p docs/{architecture,api,deployment,troubleshooting}
mkdir -p logs
mkdir -p config

# Create __init__.py files for Python packages
echo "📝 Creating Python package files..."
touch backend/__init__.py
touch backend/api/__init__.py
touch backend/services/__init__.py
touch backend/models/__init__.py
touch backend/utils/__init__.py
touch backend/config/__init__.py
touch backend/schemas/__init__.py
touch kafka/__init__.py
touch kafka/producers/__init__.py
touch kafka/consumers/__init__.py
touch kafka/config/__init__.py
touch analytics/__init__.py
touch analytics/baseline/__init__.py
touch analytics/anomaly/__init__.py
touch analytics/forecast/__init__.py
touch dashboard/__init__.py
touch dashboard/utils/__init__.py
touch dashboard/pages/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

echo "✅ Folder structure created successfully!"
ls -la

