<div style="display: flex; justify-content: center; align-items: center;">
  <img
    src="https://docs.arcade.dev/images/logo/arcade-logo.png"
    style="width: 250px;"
  >
</div>

<div style="display: flex; justify-content: center; align-items: center; margin-bottom: 8px;">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python version" style="margin: 0 2px;">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" style="margin: 0 2px;">
  <img src="https://img.shields.io/pypi/v/arcade_zendesk" alt="PyPI version" style="margin: 0 2px;">
</div>


<br>
<br>

# Arcade Zendesk Toolkit

The Arcade Zendesk toolkit provides tools to interact with Zendesk Help Center, enabling you to search and retrieve knowledge base articles.

## Features

- **Article Search**: Search for Help Center articles with powerful filtering options
  - Full-text search across article content and titles
  - Filter by categories, sections, labels, and dates
  - Sort by relevance, creation date, or update date
  - Flexible pagination support
  - HTML content cleaning and truncation

## Installation

```bash
pip install arcade-zendesk
```

## Configuration

Before using the toolkit, you need to configure your Zendesk credentials:

1. Set up OAuth2 authentication for Zendesk
2. Configure the `ZENDESK_SUBDOMAIN` secret with your Zendesk subdomain

## Usage

### Search Articles

```python
from arcade_zendesk.tools import search_articles
from arcade_tdk import ToolContext

# Basic search
result = await search_articles(
    context=context,
    query="password reset",
    per_page=10
)

# Advanced search with filters
result = await search_articles(
    context=context,
    query="API documentation",
    category=123,
    created_after="2024-01-01",
    sort_by="created_at",
    sort_order="desc",
    all_pages=True
)

# Search by labels (Professional/Enterprise only)
result = await search_articles(
    context=context,
    label_names="windows,setup",
    query="installation"
)
```

### Search Parameters

- `query`: Search text to match against articles
- `label_names`: Comma-separated list of label names (Professional/Enterprise only)
- `category`: Filter by category ID
- `section`: Filter by section ID
- `created_after/before/at`: Filter by creation date (YYYY-MM-DD format)
- `sort_by`: Sort by 'created_at' only
- `sort_order`: Sort order 'asc' or 'desc'
- `per_page`: Number of results per page (max 100)
- `all_pages`: Automatically fetch all available pages
- `max_pages`: Maximum number of pages to fetch
- `include_body`: Include article body content in results

## Development

### Setup

```bash
# Install with local sources
make install-local

# Install from PyPI
make install
```

### Testing

```bash
# Run tests
make test

# Run linting and type checking
make check

# Run coverage report
make coverage
```

### Building

```bash
# Build the package
make build
```

### Evaluations

Run tool evaluations:
```bash
make eval
```

## Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md).

Quick deployment:
```bash
# Deploy using the main worker configuration
cd ../
arcade deploy

# Or create your own worker configuration
arcade deploy --config zendesk-worker.toml
```

## Contributing

Read the docs on how to create a toolkit [here](https://docs.arcade.dev/home/build-tools/create-a-toolkit)
