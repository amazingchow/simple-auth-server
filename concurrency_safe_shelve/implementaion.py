# -*- coding: utf-8 -*-
import builtins
import fcntl
import shelve
import types
from fcntl import LOCK_EX
from fcntl import LOCK_NB
from fcntl import LOCK_SH
from fcntl import LOCK_UN


def _close_thread_safe_shelf(self):
    shelve.Shelf.close(self)
    if self.refs > 0:
        lck_flags = LOCK_UN  # unlock
        fcntl.flock(self.lck_file.fileno(), lck_flags)
        self.lck_file.close()
    self.refs -= 1


def open_thread_safe_shelf(filename, flag="c", protocol=None, writeback=False, block=True):
    """
    Open the shelve file, create a lock file at ${filename}.lck.
    If block is set to be False, then a IOError will be raised if the lock cannot be acquired.
    """
    lck_filename = filename + ".lck"
    lck_file = builtins.open(lck_filename, "w")

    lck_flags = LOCK_EX  # acquire a shared lock
    if flag == "r":
        lck_flags = LOCK_SH  # acquire an exclusive lock
    if not block:
        lck_flags = lck_flags | LOCK_NB
    fcntl.flock(lck_file.fileno(), lck_flags)

    shelf = shelve.open(filename, flag, protocol, writeback)

    # override the close method
    shelf.close = types.MethodType(_close_thread_safe_shelf, shelf)
    shelf.lck_file = lck_file
    # since both shelf.__exit__ and shelf.__del__ will do shelf.close, we should handle the case
    shelf.refs = 1

    return shelf
