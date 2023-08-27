from threading import Thread
from time import sleep
from typing import Any, Callable


class QueueError(Exception):
    pass


class Queue:
    def __init__(self):
        self.__queue__ = []
        self.__is_listening__ = False

    @property
    def is_listening(self):
        return self.__is_listening__

    @property
    def is_empty(self) -> bool:
        """Property to check if queue is empty.

        Returns:
            bool: True if queue is empty else False
        """
        return len(self.__queue__) <= 0

    def enqueue(self, item: Any):
        self.__queue__.append(item)

    def dequeue(self, handler: Callable) -> Any:
        if self.is_empty:
            raise QueueError("can't get elements out of empty Queue")
        value = self.__queue__.pop(0)
        handler_return = handler(value)
        return handler_return

    def __listner_func__(self, handler: Callable, timeout: float = 10.0):
        while True:
            try:
                self.dequeue(handler)
            except QueueError:
                sleep(timeout)

    def listener(self, handler: Callable, timeout: float = 1.0):
        """A lister function for listening on the queue

        Args:
            handler (Callable): _description_
            timeout (float, optional): _description_. Defaults to 10.0.
        """
        if self.is_listening:
            return
        thread = Thread(target=self.__listner_func__, args=(handler, timeout))
        thread.start()
        self.__is_listening__ = True
