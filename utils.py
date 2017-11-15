# -*- coding: utf-8 -*-

import re
from math import sqrt
from operator import itemgetter


class PersonsInfo:
  """
  Класс сохраняет информацию о персонах (имя и координаты x;y). Также он предоставляет возможность найти
  k-ближайших соседей.
  """
  MAX_NEIGHBORHOOD_NUM = 100

  def __init__(self):
    self.persons = []

  def add_person(self, name, x, y):
    """
    Метод сохраняет в объект класса персону с переданными параметрами.

    :param name: имя персоны
    :param x: x-координата
    :param y: y-координата
    :return:
    """
    self.persons.append((name, (x, y)))

  def query_knn(self, x, y, k):
    """
    Метод возвращает k ближайших соседей (в качестве меры расстояния используем представленный self.dist функционал)
    переданным координатам.

    :param x: x-координата для поиска
    :param y: y-координата для поиска
    :param k: количество ближайших к (x, y) точек (должно быть от 0 до self.MAX_NEIGHBORHOOD_NUM)
    :return: имена ближайших к (x, y) персон.
    """
    if not (0 <= k <= self.MAX_NEIGHBORHOOD_NUM):
      raise Exception("Number of neighborhoods should be greater than 0 and less than %i" % self.MAX_NEIGHBORHOOD_NUM)
    dist_dict = [(self.dist((x, y), person_data[1]), person_data[0]) for person_data in self.persons]
    return [person[1] for person in sorted(dist_dict, key=itemgetter(0))[:k]]

  def dist(self, a, b):
    """
    Метод для расчета расстояния от точки a до точки b

    :param a: (tuple) двумерная точка
    :param b: (tuple) двумерная точка
    :return: эвклидово расстояние между точками a и b
    """
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


_retype = type(re.compile(''))


def custom_handler(obj):
  """
  Специальный метод для параметра default метода json.dumps
  :param obj: объект, к которому нужно применить определенное изменение (в завимости от типа)
  :return: преобразованний к нужному формату obj
  """
  if hasattr(obj, 'isoformat') and callable(getattr(obj, 'isoformat')):
    return obj.isoformat()
  if obj.__class__.__name__ == "ObjectId":
    return str(obj)
  if obj.__class__ is set:
    return list(obj)
  if obj.__class__ is _retype:
    return obj.pattern
