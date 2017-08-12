"""
Logger Mixin
Its important to use logger in the code and making sure Logger is configured
"""
from logging import Logger


from core.exceptions import ImproperException


class LoggerMixin(object):
    """
    Logger Mixin, which will be inherited in all Services.
    """
    logger = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validate()

    def logger_info(self, message):
        """Info Log"""
        self.logger.info(message)

    def logger_error(self, message):
        """Error Log"""
        self.logger.error(message)

    def logger_warning(self, message):
        """Warning Log"""
        self.logger.warning(message)

    def logger_debug(self, message):
        """Debug Log"""
        self.logger.debug(message)

    def validate(self):
        """Checks if logger is defined"""
        if not self.logger and not isinstance(sel.logger, Logger):
            raise ImproperException(
                "Logger not initiated for class: {}"
                .format(self.__class__.__name__)
            )
