# -*- coding: utf-8 -*-

import random
import time

from utils import PersonsInfo


def generate_data(elements_number, centers_number):
  data = []
  for center_num in range(centers_number):
    centerX, centerY = random.random() * 10000.0, random.random() * 10000.0
    for element_num in range(elements_number):
      data.append(("%i_%i" % (center_num, element_num), random.gauss(centerX, 1000), random.gauss(centerY, 1000)))
  return data


def test_coord(persons_info, x, y, k=100):
  return persons_info.query_knn(x, y, k)


if __name__ == "__main__":
  generated_data = generate_data(3000, 200)
  persons_info = PersonsInfo()
  for generated_person in generated_data:
    persons_info.add_person(generated_person[0], generated_person[1], generated_person[2])
  start_time = time.time()
  test_x = random.random() * 10000.0
  test_y = random.random() * 10000.0
  knn = test_coord(persons_info, test_x, test_y)
  end_time = time.time()
  print end_time - start_time
