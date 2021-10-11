#!/usr/bin/env python3

# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Crappy fuzzing script to try to trigger some UA-CH GREASE breakage."""

from random import choice, random
from time import sleep

import requests
from tranco import Tranco

import argparse

greasey_chars = "_ ( ) ; ? = - : . /"
greasey_list = greasey_chars.split(' ')

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
  'sec-fetch-mode': 'navigate'
}

t = Tranco(cache=True, cache_dir='.tranco')
tranco_list = t.list()

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--top_n_sites",
                     help="The top N sites, as listed by Tranco",
                     default=1000, type=int)
args = parser.parse_args()

print(f'running on top {args.top_n_sites} sites')
for site in tranco_list.top(args.top_n_sites):
  for candidate in greasey_list:
      greasey_header = f'{candidate}Not{choice(greasey_list)}A{choice(greasey_list)}Brand'
      headers.update({'Sec-CH-UA': greasey_header})
      try:
          # in theory this should follow redirects.
          r = requests.get(f'http://{site}', headers=headers)
          print(f'{r.status_code} with {candidate} on {site} using {r.request.headers["Sec-CH-UA"]}')
          try:
              r.raise_for_status()
          except requests.exceptions.HTTPError as e:
              # probably logging to disk is nicer?
              print(f'!!!{r.status_code} with {candidate} on {site} using {r.request.headers["Sec-CH-UA"]}')
      except:
          print(f"Skipping {site} because it's being weird?")
          continue
      sleep(random() + 0.25)
