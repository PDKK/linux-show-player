# -*- coding: utf-8 -*-
#
# This file is part of Linux Show Player
#
# Copyright 2012-2016 Francesco Ceruti <ceppofrancy@gmail.com>
#
# Linux Show Player is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Linux Show Player is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Linux Show Player.  If not, see <http://www.gnu.org/licenses/>.

import logging
import traceback
from functools import wraps, partial
from threading import Thread, Lock, RLock

_synchronized_meta_lock = Lock()


def async(target):
    """Decorator. Make a function asynchronous.

    The target function is executed in a differed thread.
    """

    @wraps(target)
    def wrapped(*args, **kwargs):
        Thread(target=target, args=args, kwargs=kwargs, daemon=True).start()

    return wrapped


def async_in_pool(pool):
    """Decorator. Make a function asynchronous in a specified pool.

    The target function is executed in the specified threads-pool.

    .. Usage::

        class MyClass:
            __MyPool = ThreadPoolExecutor(10)

            @async_in_pool(__MyPool)
            def do_some_task(self):
                pass

    """

    def decorator(target):
        @wraps(target)
        def wrapped(*args, **kwargs):
            pool.submit(target, *args, **kwargs)

        return wrapped

    return decorator


def synchronized_function(target=None, *, blocking=True, timeout=-1):
    """Decorator. Make a *function* synchronized.

    Only one thread at time can enter the decorated function, but the same
    thread can reenter.
    """

    if target is None:
        return partial(synchronized_function, blocking=blocking,
                       timeout=timeout)

    target.__lock__ = RLock()

    @wraps(target)
    def synchronized(*args, **kwargs):
        try:
            if target.__lock__.acquire(blocking=blocking, timeout=timeout):
                return target(*args, **kwargs)
            else:
                return
        finally:
            try:
                target.__lock__.release()
            except RuntimeError:
                pass

    return synchronized


def synchronized_method(target=None, *, lock_name=None, blocking=True,
                        timeout=-1):
    """Decorator. Make a *method* synchronized.

    Only one thread at time can access the decorated method, but the same
    thread can reenter.

    If in the same object more the one method is decorated with the same
    lock_name, those will share the same lock.
    If no lock_name is specified one will be generated based on the method name.

    ..note:
        The lock is created automatically by the method, but, if needed, can
        be "manually" created by the user as an object attribute named as same
        as lock_name.

    """

    # If called with (keywords) arguments
    if target is None:
        return partial(synchronized_method, lock_name=lock_name,
                       blocking=blocking, timeout=timeout)

    if not isinstance(lock_name, str):
        # generate a lock_name like "__method_name_lock__"
        lock_name = '__' + target.__name__ + '_lock__'

    @wraps(target)
    def wrapped(self, *args, **kwargs):
        with _synchronized_meta_lock:
            lock = getattr(self, lock_name, None)

            # If the lock is not defined, then define it
            if lock is None:
                lock = RLock()
                setattr(self, lock_name, lock)

        try:
            if lock.acquire(blocking=blocking, timeout=timeout):
                return target(self, *args, **kwargs)
            else:
                return
        finally:
            try:
                lock.release()
            except RuntimeError:
                pass

    return wrapped


def suppress_exceptions(target=None, *, log=True):
    """Decorator. Suppress all the exception in the decorated function.

    :param log: If True (the default) exceptions are logged as warnings.
    """

    if target is None:
        return partial(suppress_exceptions, print_exc=log)

    @wraps(target)
    def wrapped(*args, **kwargs):
        try:
            return target(*args, **kwargs)
        except Exception:
            logging.warning('Exception suppressed:\n' + traceback.format_exc())

    return wrapped


def memoize(obj):
    """Decorator. Caches a function's return value each time it is called.

    If called later with the same arguments, the cached value is returned
    (not reevaluated).

    .. Note::
        This works for any callable object.
        The arguments are cached (as strings) in object.cache.
    """
    cache = obj.cache = {}

    @wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]

    return memoizer


def typechecked(target):
    """Decorator. Check a function arguments types at runtime.

    Annotations are used for checking the type (e.g. def fun(a: int, b: str)),
    this decorator should be used only if really needed, duck typing is the
    python-way, furthermore this will add a little overhead.
    """

    @wraps(target)
    def wrapped(*args, **kwargs):
        for index, name in enumerate(target.__code__.co_varnames):
            annotation = target.__annotations__.get(name)
            # Only check if annotation exists and a type
            if isinstance(annotation, type):
                # First len(args) are positional, after that keywords
                if index < len(args):
                    value = args[index]
                elif name in kwargs:
                    value = kwargs[name]
                else:
                    continue

                if not isinstance(value, annotation):
                    raise TypeError('Incorrect type for "{0}"'.format(name))

        return target(*args, **kwargs)

    return wrapped
