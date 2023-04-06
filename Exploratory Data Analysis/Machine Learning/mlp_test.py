"""
Jack Bosco
3/6/2023
"""
from modules.utils.mlp import *
from modules.utils.trainLoader import loadData
from modules.utils.misc import section
import sys
import torch
import os
import numpy as np
import pandas as pd

dir = os.path.join('precomp', 'deeptest')
T, I = loadData(60, 'testData')

def precompTest():
	#load the data from the tester
	new = []
	for t in T:
		if t == 215:
			new.append([0, 1])
		else:
			new.append([1, 0])
	T = np.array(new)

	np.save(os.path.join(dir, 'targets'), T)
	np.save(os.path.join(dir, 'inputs'), I)

test_dataset = SpiderDataset(dir, dir)
test_loader = DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

dev = 'cuda' if torch.cuda.is_available() else 'cpu'

filePath = os.path.join('precomp', 'deepsave', 'deepMLP.pt')

classifier = BaseClassifier(in_dim=216, feature_dim=128, out_dim=2)
classifier = classifier.to(dev)

def test(test_loader, statedict_path, loss_fn=None, classifier=None):
	classifier.load_state_dict(torch.load(statedict_path))
	classifier.eval()
	fpos, fneg = 0, 0
	pos, neg = 0, 0
	ncorrect = 0
	outs = []

	with torch.no_grad():
		i=0
		for data, target in test_loader:
			data = data.to(dev)
			target = target.to(dev)
			#print(data.shape, target.shape)
			data = data.flatten(start_dim=1)
			out = classifier(data)
			#print(out, target)
			predDead = out[0][0] > out[0][1]
			if target[0][1] == 1: # spider is alive
				neg += 1
				if not predDead:
					ncorrect += 1
				else:
					fpos += 1
			elif target[0][1] == 0:
				pos += 1
				if predDead:
					ncorrect += 1
				else:
					fneg += 1
			wrong = '*' if (predDead and target[0][1] == 1) or (not predDead and target[0][1] == 0) else ' '
			outs.append([str(round(float(out[0][0]), 2)) + ' : ' + str(round(float(out[0][1]), 2)), T[i], wrong])
			i += 1
	df = pd.DataFrame(data=outs, columns=['MLP Output', 'Time of Death', 'wrong?'])
	print('\n', section('Deep Perceptron'))
	print('Left > Right : spider predicted "DEAD"')
	print('False Positives:', str(fpos)+'/'+str(neg), 'False Negatives:', str(fneg)+'/'+str(pos))
	print('Total Accuracy:', str(100*ncorrect/len(test_dataset)) + '%')
	print(df)

test(test_loader=test_loader, statedict_path=filePath, classifier=classifier)