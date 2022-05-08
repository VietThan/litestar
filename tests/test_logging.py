import logging
from unittest.mock import Mock, patch

from _pytest.logging import LogCaptureFixture

from starlite import create_test_client
from starlite.logging import LoggingConfig


@patch("logging.config.dictConfig")
def test_logging_debug(dict_config_mock: Mock) -> None:
    config = LoggingConfig()
    config.configure()
    assert dict_config_mock.mock_calls[0][1][0]["loggers"]["starlite"]["level"] == "INFO"
    dict_config_mock.reset_mock()


@patch("logging.config.dictConfig")
def test_logging_startup(dict_config_mock: Mock) -> None:
    logger = LoggingConfig(loggers={"app": {"level": "INFO", "handlers": ["console"]}})
    with create_test_client([], on_startup=[logger.configure]):
        assert dict_config_mock.called


config = LoggingConfig(root={"handlers": ["queue_listener"], "level": "WARNING"})
config.configure()
logger = logging.getLogger()


def test_queue_logger(caplog: LogCaptureFixture) -> None:
    """
    Test to check logging output contains the logged message
    """
    caplog.set_level(logging.INFO)
    logger.info("Testing now!")
    assert "Testing now!" in caplog.text


def test_queue_logger_handler_resolve_handler() -> None:
    """
    Tests resolve handler
    """
    handlers = logger.handlers
    assert isinstance(handlers[0].handlers[0], logging.StreamHandler)  # type: ignore
    logger.handlers[0].stop()  # type: ignore
