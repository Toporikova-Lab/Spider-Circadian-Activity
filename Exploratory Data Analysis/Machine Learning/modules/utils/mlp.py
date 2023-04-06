"""
Jack Bosco
3/6/2023
"""
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torch.nn import Softmax
from torchvision import transforms
from torch import optim
from torch.utils.data import Dataset, DataLoader
from torchvision.datasets import MNIST
from torchvision.transforms import ToTensor

torch.manual_seed(0) # for reproducability
dev ='cuda' if torch.cuda.is_available() else 'cpu'

"""
First download files for use in custom ImageDataset example
"""

class SpiderDataset(Dataset):
	def __init__(self, target_dir, data_dir, transform=None, target_transform=None):
		self.data_path = os.path.join(data_dir, 'inputs.npy')
		self.target_path = os.path.join(target_dir, 'targets.npy')

		self.inputs = np.load(self.data_path, allow_pickle=True)
		self.inputs = torch.tensor(self.inputs, device=dev, dtype=torch.float)
		self.targets = np.load(self.target_path, allow_pickle=True)
		self.targets = torch.tensor(self.targets, device=dev, dtype=torch.float)

		self.transform = transform
		self.target_transform = target_transform
	
	def __getitem__(self, idx):
		inp = self.inputs[idx]
		tar = self.targets[idx]
		return inp, tar	
	
	def __len__(self):
		return len(self.targets)

"""
Build MNIST Classifier in PyTorch
"""
	
class BaseClassifier(nn.Module):
	def __init__(self, in_dim, feature_dim, out_dim):
		super(BaseClassifier, self).__init__()
		self.classifier = nn.Sequential(
						nn.Linear(in_dim, feature_dim, bias=True, dtype=torch.float),
						nn.ReLU(),
						nn.Linear(feature_dim, out_dim, bias=True, dtype=torch.float),
						nn.Softmax(dim=1)
		)
		self.flatten = nn.Flatten()
		
	def forward(self, x):
		x = self.flatten(x)
		logits = self.classifier(x)
		return logits
	
