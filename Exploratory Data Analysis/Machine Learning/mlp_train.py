"""
Jack Bosco
3/6/2023
"""
from modules.utils.mlp import *
from torch import optim
from modules.utils.trainLoader import loadData
import sys
import numpy as np
import torch
from modules.utils.misc import progressBar

dir = os.path.join('precomp', 'deeptrain')

def precompTest():
	# load input patterns for the training data
	T, I = loadData(60, 'trainData')

	# convert targets into dead|not-dead
	new = []
	for t in T:
		if t == 215:
			new.append([0, 1])
		else:
			new.append([1, 0])
	T = np.array(new)

	ext = '0'
	while 'inputs' + ext + '.npy' in os.listdir(dir):
		ext = str(int(ext)+1)

	np.save(os.path.join(dir, 'targets'+ext), T)
	np.save(os.path.join(dir, 'inputs'+ext), I)

train_dataset = SpiderDataset(dir, dir)
train_loader = DataLoader(dataset=train_dataset, batch_size=2, shuffle=True)

# Instantiate model, optimizer, and hyperparameter(s)
in_dim, feature_dim, out_dim = 216, 128, 2
loss_fn = nn.CrossEntropyLoss()
epochs=500
lr =  1e-4
momentum = 0.9
weight_decay = 0.1
classifier = BaseClassifier(in_dim, feature_dim, out_dim)

dev = 'cuda' if torch.cuda.is_available() else 'cpu'
print('running on ' + dev)
print('training for', epochs, 'epochs')
print('learning rate:', lr)
print('momentum:', momentum)
print('weight decay:', weight_decay)

classifier = classifier.to(dev)
	
def train(epochs, batch_size\
		, train_loader, plot=False, lr = 1e-3\
		, loss_fn=None, mom=1, wd=1):
	classifier.train()
	optimizer = optim.SGD(classifier.parameters(), lr=lr, momentum=mom, weight_decay=wd)
	loss_lt = []
	for epoch in range(epochs):
		if epoch % (epochs / 100) == 0:
			print(progressBar(epoch/epochs, message='Training DEEP'), end='\r')
		elif epoch + 1 == epochs:
			print(progressBar(message='DONE'))
		running_loss = 0.0
		for minibatch in train_loader:
			data, target = minibatch
			#print(data.shape, target.shape)
			data = data.flatten(start_dim=1)

			data = data.to(dev)
			target = target.to(dev)

			out = classifier(data)
			computed_loss = loss_fn(out, target)
			computed_loss.backward()
			optimizer.step()
			optimizer.zero_grad()
			
			# Keep track of sum of loss of each minibatch
			running_loss += computed_loss.item()
		loss_lt.append(running_loss/len(train_loader))
		#print("Epoch: {} train loss: {}".format(epoch+1, running_loss/len(train_loader)))
	
	if plot:
		plt.plot([i for i in range(1,epochs+1)], loss_lt)
		plt.xlabel("Epoch")
		plt.ylabel("Training Loss")
		plt.title("MNIST Training Loss: optimizer {}, lr {}, momentum {}, weight decay {}".format("SGD", lr, mom, wd))

	#for saving the state dict
	dir = os.path.join('precomp', 'deepsave')
	ext = '0'
	while 'deepMLP' + ext + '.pt' in os.listdir(dir):
		ext = str(int(ext)+1)

	# Save state to file as checkpoint
	torch.save(classifier.state_dict(), os.path.join(dir, 'deepMLP' + ext + '.pt'))
	plt.savefig(os.path.join(dir, 'learning' + ext + '.png'))

train(plot=True,epochs=epochs, batch_size=2, train_loader=train_loader, lr=lr, loss_fn=loss_fn,
	   mom=momentum, wd=weight_decay)
