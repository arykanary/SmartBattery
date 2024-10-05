from datetime import datetime, timedelta
import time
from functools import wraps
from typing import Any, Union, Tuple


class Throttle:
    """Decorator that prevents a function from being called more than once every time period.

    To create a function that cannot be called more than once a minute:
    
    >>> @throttle(minutes=1)
    >>> def my_fun():
    >>>     pass

    https://gist.github.com/ChrisTM/5834503
    """
    def __init__(self, seconds=0, minutes=0, hours=0):
        """

        Args:
            seconds (int, optional): _description_. Defaults to 0.
            minutes (int, optional): _description_. Defaults to 0.
            hours (int, optional): _description_. Defaults to 0.
        """
        self.throttle_period = timedelta(seconds=seconds, minutes=minutes, hours=hours)
        self.time_of_last_call = datetime.min

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            now = datetime.now()
            time_since_last_call = now - self.time_of_last_call

            if time_since_last_call > self.throttle_period:
                self.time_of_last_call = now
                return fn(*args, **kwargs)

        return wrapper


def wait(dt):
    while True:
        if datetime.now() >= dt:
            break


class Timer:
    """time.sleep but better"""
    def __init__(self, frequency: Union[timedelta, Tuple[timedelta]]=timedelta(minutes=1), start: datetime=datetime.now()):
        """_summary_

        Args:
            frequency (Union[timedelta, Tuple[timedelta]], optional): _description_. Defaults to timedelta(minutes=1).
            start (datetime, optional): _description_. Defaults to datetime.now().
        """        
        if isinstance(frequency, tuple):
            self.frequency = frequency
        elif isinstance(frequency, timedelta):
            self.frequency = (frequency, )
        
        self.start = start
                
    def __call__(self, func):

        def wrapper(*arg, **kwargs):
            start = self.start

            while True:
                for freq in self.frequency:
                    func(*arg, **kwargs)

                    nex = start + freq
                    wait(nex)
                    start = nex

        return wrapper
    


if __name__ == "__main__":
    @Timer((timedelta(seconds=2), timedelta(seconds=1)))
    def some_func(name='Some'):
        print(time.time(), name)
        time.sleep(.5)
    
    some_func()
    