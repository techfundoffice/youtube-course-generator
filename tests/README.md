# Test Structure Documentation

## Overview
This testing framework follows a well-organized structure that separates different types of tests for better maintainability and clarity.

## Directory Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests - test individual components
│   ├── test_validators.py   # Validation utility tests
│   └── test_services.py     # Service layer tests
├── integration/             # Integration tests - test component interactions
│   └── test_app_routes.py   # Flask route and API tests
├── functional/              # End-to-end tests - test complete workflows
│   └── test_course_generation.py  # Complete course generation workflow
└── README.md               # This documentation
```

## Test Categories

### Unit Tests (`tests/unit/`)
- Test individual functions and classes in isolation
- Fast execution with mocked dependencies
- Focus on logic validation and edge cases
- Examples: validators, utility functions, service methods

### Integration Tests (`tests/integration/`)
- Test interactions between components
- Verify API endpoints and route handlers
- Test database operations and external service integrations
- Examples: Flask routes, service interactions

### Functional Tests (`tests/functional/`)
- Test complete user workflows end-to-end
- Verify business requirements and user scenarios
- May be slower but provide high confidence
- Examples: full course generation pipeline

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Functional tests only
pytest tests/functional/
```

### Run with Markers
```bash
# Run only fast tests
pytest -m "not slow"

# Run only unit tests
pytest -m unit

# Run with coverage
pytest --cov=. --cov-report=html
```

## Test Fixtures

All shared fixtures are defined in `conftest.py`:
- `test_app`: Flask application configured for testing
- `client`: Test client for making HTTP requests
- `mock_*_service`: Mocked service instances
- `sample_*_data`: Test data fixtures

## Best Practices

1. **Test Naming**: Use descriptive names that explain what is being tested
2. **Test Independence**: Each test should be able to run independently
3. **Mock External Dependencies**: Use mocks for external APIs and services
4. **Clear Assertions**: Use specific assertions with helpful error messages
5. **Test Data**: Use the provided fixtures for consistent test data

## Configuration

The pytest configuration is in `pytest.ini`:
- Async test support enabled
- Coverage reporting configured
- Warning filters to reduce noise
- Custom markers for test categorization

## Adding New Tests

1. Choose the appropriate directory based on test type
2. Follow existing naming conventions
3. Use shared fixtures from `conftest.py`
4. Add appropriate markers (`@pytest.mark.unit`, `@pytest.mark.integration`, etc.)
5. Mock external dependencies appropriately

This organized structure makes tests easier to find, run, and maintain while providing clear separation of concerns.