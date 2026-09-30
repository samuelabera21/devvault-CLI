import logging

from devvault.logging_config import RedactingFormatter, setup_logging


def test_redacting_formatter():
    formatter = RedactingFormatter(fmt="%(message)s")
    record = logging.LogRecord(
        name="devvault",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Connecting password=SuperSecretPassword123 token: my_secret_token",
        args=(),
        exc_info=None,
    )

    formatted = formatter.format(record)
    assert "SuperSecretPassword123" not in formatted
    assert "my_secret_token" not in formatted
    assert "password=********" in formatted


def test_setup_logging():
    setup_logging(verbose=True, quiet=False)
    logger = logging.getLogger("devvault")
    assert logger.level == logging.DEBUG

    setup_logging(verbose=False, quiet=True)
    assert logger.level == logging.ERROR
