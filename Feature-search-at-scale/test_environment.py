import sys
import time


print("Python version", sys.version)


import numpy as np
import scipy as scp
from matplotlib import pyplot as plt
import faiss


import torch
import torchvision


print(np.__version__)
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())
print(faiss.__version__)
print(torchvision.__version__)
