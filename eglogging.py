# wrapper around python's logging module

import logging
import logging.config
import json
import inspect
import os

# set what will get imported when someone writes "from eglogging import *"
__all__ = [ 'MSG', 'INFO', 'DEBUG', 'WARN', 'ERROR', 'CRITICAL', 'LOG',
            'logging_load_config_from_file',
            'LOG_COLORS' ]

DEFAULT_CONFIG_FILENAME = 'logger_config_DEFAULT.json'
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   DEFAULT_CONFIG_FILENAME)

# some shorthand accessors
def MSG(m, color = None):
  Eglogging._log(logging.INFO, m, color = color)
  return

def INFO(m, color = None):
  Eglogging._log(logging.INFO, m, color = color)
  return

def DEBUG(m, color = None):
  Eglogging._log(logging.DEBUG, m, color = color)
  return

def WARN(m, color = None):
  Eglogging._log(logging.WARNING, m, color = color)
  return

def ERROR(m, color = None):
  Eglogging._log(logging.ERROR, m, color = color)
  return

def CRITICAL(m, color = None):
  Eglogging._log(logging.CRITICAL, m, color = color)
  return

def LOG(m, level = logging.NOTSET, color = None):
  Eglogging._log(level, m, color)
  return

def logging_load_config_from_file(filename):
  Eglogging.load_config_from_file(filename)
  return



# colors
LOG_COLORS = { 'GRAY'  : "\x1b[38;21m",
               'GREEN' : "\x1b[1;32m",
               'ORANGE': "\x1b[33;1m",
               'RED'   : "\x1b[31;1m",
               'RESET' : "\x1b[0m" }



class Eglogging(object):
  """wrapper around python's logging module"""

  # make the logger variable static
  logger = None

  @staticmethod
  def load_config_from_file(filename):
    'load logging config from a json file'

    with open(filename, 'r') as f:
      config_dict = json.load(f)

    logging.config.dictConfig(config_dict)

    # get the logger
    Eglogging.logger = logging.getLogger(__name__) # __name__ is eglogging
    return


  @staticmethod
  def _log(level, m, color = None):
    # log message m at the info level

    # if the user didn't specify a color,
    # set it based on the message level
    if color is None:
      if level >= logging.ERROR:
        color = LOG_COLORS['RED']
      elif level >= logging.WARNING:
        color = LOG_COLORS['ORANGE']
      else:
        color = LOG_COLORS['GRAY']

    myfields = { 'line'       : Eglogging._line_info(),
                 'color_code' : color,
                 'color_reset': LOG_COLORS['RESET'] }

    Eglogging.logger.log(level, m, extra = myfields)



  @staticmethod
  def _line_info():
    '''
    get the file and line number from which stuff is getting logged
    formatted like filename:NN
    '''
    try:
      stack = inspect.stack()
      frame = stack[3]

      # filename: only show the last part
      fn = frame[1]
      slash = fn.rfind('/')
      if slash != -1:
        fn = fn[slash + 1 :]

      return "{}:{}".format(fn, frame[2])

    except Exception as e:
      print("Exception encountered in line_info(): {}".format(e))
      return "ERROR"



########################## INITIALIZE THE LOGGER ###############################
Eglogging.load_config_from_file(DEFAULT_CONFIG_PATH)
