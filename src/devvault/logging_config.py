import logging
import re


class RedactingFormatter(logging.Formatter):
    """Logging formatter that redacts secrets and authentication credentials."""

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        msg = re.sub(
            r"(?i)(password|secret|token|api[_-]?key|auth)[\s:=]+([^\s,]+)",
            r"\1=********",
            msg,
        )
        msg = re.sub(r"gAAAA[a-zA-Z0-9_\-=]+", "********", msg)
        return msg


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Configure application logging level and safe redacting formatter."""
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO

    handler = logging.StreamHandler()
    formatter = RedactingFormatter(
        fmt="[%(levelname)s] %(name)s: %(message)s" if verbose else "%(message)s"
    )
    handler.setFormatter(formatter)

    root_logger = logging.getLogger("devvault")
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.propagate = False
