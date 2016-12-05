import pandas as pd
import json
from pandas import DataFrame

path = 'F:/code/xiaoqu/xiaoqu.json'

data = [json.loads(line) for line in open(path,'r')]

df = DataFrame(data)