'''
  - Python module to encapsulate the thread class into a one killable

	Copyright (C) 2021 Alejandro Iregui Valcarcel

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import threading
from demos.demo3d import *
from demos.game import *
import ctypes

class StoppableThread(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)

  def get_id(self):
    # returns id of the respective thread
    if hasattr(self, '_thread_id'):
      return self._thread_id
    for id, thread in threading._active.items():
      if thread is self:
        return id

  def raise_exception(self):
    thread_id = self.get_id()
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
        ctypes.py_object(SystemExit))
    if res > 1:
      ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
      print('Exception raise failure')

class StoppableThreadGame(StoppableThread):
  def __init__(self, port, treshold):
    StoppableThread.__init__(self)
    self.port = port
    self.treshold = treshold

  def run(self):
    # target function of the thread class
    try:
      game(self.port, self.treshold)

    finally:
      print('ended')

class StoppableThreadModel(StoppableThread):
  def __init__(self, port, treshold):
    StoppableThread.__init__(self)
    self.port = port
    self.treshold = treshold

  def run(self):
    # target function of the thread class
    try:
      model(self.port, self.treshold)

    finally:
      print('ended')
