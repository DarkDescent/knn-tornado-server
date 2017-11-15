# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

import tornado.httpserver
from os import makedirs
from os.path import expandvars, exists, dirname
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from handlers import PersonCreationHandler, PersonQueryHandler
from utils import PersonsInfo

logger = logging.getLogger(__name__)


class RestApplication(Application):
  """
  Класс-наследник tornado Application. Настраивает хэндлеры проекта, путь до шаблонов и css, а также создает объект
  utils.PersonsInfo и сохраняет его в свой атрибут
  """
  def __init__(self, tornado_debug=None):
    """
    Инициализация класса
    """
    handlers = [
      (r"/create", PersonCreationHandler),
      (r"/query", PersonQueryHandler)
    ]
    settings = dict(
      title="KNN",
      debug=tornado_debug or True,
    )
    super(RestApplication, self).__init__(handlers, **settings)
    self.person_data = PersonsInfo()


# запускаем сервер
if __name__ == "__main__":
  define("server_host", default="127.0.0.1", help="server host")
  define("server_port", default=8090, help="server port", type=int)
  define("logpath", default="", help="path to log file")
  define("logformat", default="%(asctime)s - %(levelname)s - %(message)s", help="format of log entries")
  define("loglevel", default="INFO", help="logging level")
  define("debug", default=True, help="debug mode", type=bool)
  options.parse_command_line()

  # инициализируем логгирование
  logfile = expandvars(options.logpath)
  log_dir = dirname(logfile)
  if log_dir and not exists(log_dir):
    makedirs(log_dir)

  # очищаем логи
  root = logging.getLogger()
  for handler in root.handlers or []:
    root.removeHandler(handler)

  logging.basicConfig(filename=logfile, level=logging.getLevelName(options.loglevel or "INFO"),
                      format=options.logformat, filemode="w")
  rfh = RotatingFileHandler(logfile, mode='a', maxBytes=1024 * 1024 * 2, backupCount=1, encoding="utf8")
  logging.getLogger().addHandler(rfh)

  application = RestApplication(options.debug)

  print "server starting on port %i" % options.server_port

  logger.info("server starting on port %i" % options.server_port)

  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(options.server_port, address=options.server_host)
  IOLoop.instance().start()
