# -*- coding: utf-8 -*-

import json
import logging

from tornado.web import RequestHandler

from utils import custom_handler

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
  """
  Базовый хэндлер для хэндлеров проекта. Содержит метод write_json (возвращает сдампленные в json данные по запросу к
  Tornado) и property persons_data - объект класса utils.PersonsInfo
  """
  @property
  def persons_data(self):
    return self.application.person_data

  def write_json(self, results):
    self.set_header("Content-Type", "application/json; charset=UTF-8")
    self.finish(json.dumps(results, default=custom_handler, sort_keys=False))


class PersonCreationHandler(BaseHandler):
  """
  /create
  Хэндлер отвечает за создание и сохранение персоны (имени и двумерной координаты)
  """
  def post(self):
    """
    Обработка POST-запроса
    Параметры:
      name (str) - имя персоны
      x (float) - x-координата персоны
      y (float) - y-координата персоны
    Метод добавляет запись в self.persons_data.

    :return:
    """
    person_name = self.get_argument("name")
    person_coord_x = float(self.get_argument("x"))
    person_coord_y = float(self.get_argument("y"))
    self.persons_data.add_person(person_name, person_coord_x, person_coord_y)


class PersonQueryHandler(BaseHandler):
  """
  /query
  Хэндлер пытается вернуть k ближайших к (x, y) персон. k, x, y передаются в параметрах GET-запроса.
  """
  def get(self):
    """
    Обработчик GET-запроса.
    Параметры:
      x (float) - x-координата персоны
      y (float) - y-координата персоны
      k (int) - количество ближайших точек, которые нужно вернуть.

    :return:
    """
    person_coord_x = float(self.get_argument("x"))
    person_coord_y = float(self.get_argument("y"))
    k = int(self.get_argument("k"))
    knn = self.persons_data.query_knn(person_coord_x, person_coord_y, k)
    self.write_json(knn)
