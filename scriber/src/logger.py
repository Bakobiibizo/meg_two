import logging


class Logger(logging.Logger):
    """
    Logger class for custom logging functionality.

    This class extends the built-in Logger class from the logging module and provides additional methods for logging
    errors and debug messages.

    Attributes:
        logger_name (str): The name of the logger.
        log_file_name (str): The name of the log file.
        log_level (int): The log level for the logger. Defaults to logging.INFO.
        format_str (str): The log message format string. Defaults to "%(asctime)s %(levelname)s %(message)s".

    Methods: __init__(logger_name: str, log_file_name: str, log_level: int = logging.INFO, format_str: str = "%(
    asctime)s %(levelname)s %(message)s") -> None: Initializes the Logger object.

        log_info(message, **kwargs):
            Logs an info message.

        error(message, exception=None, stack_trace=None, error_level=logging.ERROR, context=None, **kwargs):
            Logs an error message.

        debug(message, debug_level=logging.DEBUG, context=None, stack_trace=None, **kwargs):
            Logs a debug message.

        close_handlers():
            Closes the log file and stream handlers.

    """

    def __init__(
        self,
        logger_name: str,
        log_file_name: str,
        log_level: int = logging.INFO,
        format_str: str = "%(asctime)s %(levelname)s %(message)s",
    ) -> None:
        if not logging.getLogger(logger_name).handlers:
            super().__init__(name=logger_name, level=log_level)
    
            self.log_level = log_level
            self.logger_name = logger_name
            self.format_str = format_str
            self.formatter = logging.Formatter(format_str)

            self.stream_handler = logging.StreamHandler()
            self.stream_handler.setFormatter(self.formatter)
            self.addHandler(self.stream_handler)

            self.file_handler = logging.FileHandler(log_file_name)
            self.file_handler.setFormatter(self.formatter)
            self.addHandler(self.file_handler)

    def log_info(self, message, **kwargs):
        self.info(message, **kwargs)

    def error(
        self,
        message,
        exception=None,
        stack_trace=None,
        traceback=None,
        error_level=logging.ERROR,
        context=None,
        **kwargs,
    ):
        """
        Log an error message.

        Args:
            message (str): The error message.
            exception (Exception, optional): The exception object, if any. Defaults to None.
            stack_trace (str, optional): The stack trace, if any. Defaults to None.
            traceback (str, optional): The traceback, if any. Defaults to None.
            error_level (int, optional): The error level for logging. Defaults to logging.ERROR.
            context (str, optional): Additional context information. Defaults to None.
            **kwargs: Additional keyword arguments for logging.

        Raises:
            Exception: If an error occurs during the logging process.
        """
        try:
            message_parts = [message]
            if exception:
                message_parts.append(f" - Exception: {exception}")
                if stack_trace:
                    message_parts.append(f"\n{stack_trace}")
                else:
                    message_parts.append(f"\n{traceback.format_exc()}")
            if context:
                message_parts.append(f" - {context}")
            if "optional_params_str" in kwargs:
                message_parts.append(kwargs["optional_params_str"])
            message = "".join(message_parts)
            if exception:
                self.error(
                    message,
                    exception=exception,
                    stack_trace=stack_trace,
                    error_level=error_level,
                    context=context,
                    **kwargs,
                )
            else:
                self.error(
                    message,
                    stack_trace=stack_trace,
                    error_level=error_level,
                    context=context,
                    **kwargs,
                )
        except Exception:
            raise

    def debug(
        self,
        message,
        debug_level=logging.DEBUG,
        context=None,
        stack_trace=None,
        **kwargs,
    ):
        """
        Log a debug message.

        Args:
            message (str): The debug message.
            debug_level (int, optional): The debug level. Defaults to logging.DEBUG.
            context (str, optional): Additional context information. Defaults to None.
            stack_trace (str, optional): The stack trace. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the logging method.

        Raises:
            Exception: If an error occurs while logging.

        """
        try:
            final_message = message
            if context:
                final_message = f"{final_message} - {context}"
            if stack_trace:
                final_message += f"\n{stack_trace}"
            if self.isEnabledFor(debug_level):
                self.log(debug_level, final_message, **kwargs)
        except Exception as e:
            self.warning(f"Error occurred while logging: {e}")

    def close_handlers(self):
        self.removeHandler(self.stream_handler)
        self.removeHandler(self.file_handler)
        self.stream_handler.close()
        self.file_handler.close()


logger = Logger("logger", "logs.log")
