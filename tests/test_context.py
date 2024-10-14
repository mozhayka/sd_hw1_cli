import os
import pytest
from unittest.mock import patch

from cli_interpreter.context import CliContext


class TestCliContext:
    _DEFAULT_ENVS: dict[str, str] = {"foo": "bar"}

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Set up a fresh environment for each test."""
        with patch.dict(os.environ, self._DEFAULT_ENVS, clear=True):
            self.cli_context = CliContext()
            yield

    def test_initialization_with_environment_variables(self):
        """Test that the initial environment matches os.environ."""
        assert self.cli_context.env == self._DEFAULT_ENVS

    def test_set_and_get_valid_variable(self):
        """Test setting and getting a valid environment variable."""
        self.cli_context.set('TEST_VAR', 'test_value')
        assert self.cli_context.get('TEST_VAR') == 'test_value'

    def test_set_existing_variable(self):
        """Test updating an existing environment variable."""
        self.cli_context.set('TEST_VAR', 'initial_value')
        self.cli_context.set('TEST_VAR', 'updated_value')
        assert self.cli_context.get('TEST_VAR') == 'updated_value'

    def test_get_non_existent_variable(self):
        """Test getting a non-existent environment variable."""
        assert self.cli_context.get('NON_EXISTENT_VAR') == ''

    def test_set_invalid_variable_name(self):
        """Test setting an invalid environment variable name."""
        with pytest.raises(ValueError, match="Invalid environment variable name: '1INVALID_VAR'"):
            self.cli_context.set('1INVALID_VAR', 'value')

    def test_set_variable_with_special_characters(self):
        """Test setting an invalid environment variable name with special characters."""
        with pytest.raises(ValueError):
            self.cli_context.set('INVALID-VAR$', 'value')

    def test_set_variable_with_space(self):
        """Test setting an invalid environment variable name with spaces."""
        with pytest.raises(ValueError, match="Invalid environment variable name: 'INVALID VAR'"):
            self.cli_context.set('INVALID VAR', 'value')

    def test_get_variable_after_invalid_set(self):
        """Test that getting a variable after an invalid set fails gracefully."""
        self.cli_context.set('VALID_VAR', 'valid_value')
        with pytest.raises(ValueError):
            self.cli_context.set('INVALID-VAR$', 'value')
        assert self.cli_context.get('VALID_VAR') == 'valid_value'
