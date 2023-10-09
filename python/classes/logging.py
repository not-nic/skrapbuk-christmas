import queue
import time
import threading
from datetime import datetime

class Text:
    BOLD = '\033[1m'
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[36m"
    END = "\033[0m"
    YELLOW = "\033[93m"
    PURPLE = "\033[35m"

class Logging:
    _instance = None

    # Make Logging class a singleton so only once instance & message queue can exist.
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logging, cls).__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if self.__initialized:
            return
        self.__initialized = True
        self.response_queue = queue.Queue()

    def formatted_time(self):
        """
        Get the current formatted timestamp in the format: "dd/mm/YYYY - HH:MM:SS".
        """
        return datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y - %H:%M:%S")

    def info_message(self, message):
        """
        Format an INFO log message with a timestamp.
        Args: message (str): The message to be logged.
        Returns: formatted log message. (str)
        """
        return f"{Text.CYAN}{Text.BOLD}[{self.formatted_time()} INFO]: {Text.END}{message}"

    def error_message(self, message):
        """
        Format an ERROR log message with a timestamp.
        Args: message (str): The message to be logged.
        Returns: formatted log message. (str)
        """
        return f"{Text.RED}{Text.BOLD}[{self.formatted_time()} ERROR]: {Text.END}{message}"

    def queue_message(self, message, message_type):
        """
        Format and enqueue a log message based on its type.
        Args: message (str): The log message to be formatted and enqueued.
              message_type (str): Type of the log message, either 'INFO' or 'ERROR'.
        """
        response_message = None
        if message_type == 'INFO':
            response_message = self.info_message(message)
        elif message_type == 'ERROR':
            response_message = self.error_message(message)
        self.response_queue.put(response_message)

    def process_queue(self):
        """
        get log messages from the queue and print them with a 5-second delay.
        """
        while True:
            try:
                message = self.response_queue.get()
                print(message)
                time.sleep(5)
            except queue.Empty:
                break

    def start_processing_thread(self):
        """
        Start a separate thread to process log messages from the queue.
        """
        processing_thread = threading.Thread(target=self.process_queue)
        processing_thread.daemon = True
        processing_thread.start()