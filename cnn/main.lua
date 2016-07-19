----------------------------------------------------------------------
--This file is used to run all functions in this programme
--for training/testing use
--
----------------------------------------------------------------------

require 'torch'
require 'cunn'
require("cnn_model.lua")
require("cnn_loss.lua")
require("cnn_train.lua")
require("cnn_test.lua")

----------------------------------------------------------------------
-- setting parameters
print '==> processing options'

--torch.setdefaulttensortype('torch.FloatTensor')
--threads = 10
--torch.setnumthreads(threads)

seed = 1 --fixed randomization
torch.manualSeed(seed)

para = {savedir = "log/",
		optimization = 'SGD',
		loss = 'mse', -- mean square error
		trainNum = 300, -- 300 in 577
		testNum = 100, -- 277  in 577
		maxIter = 50,
		learningRate = 0.1 , -- 0.001
		weightDecay = 0,
		startAveraging = 1,
		momentum = 0,
		batchSize = 5, --100
		noutputs = 5,
		plot = false,
		save = false}

----------------------------------------------------------------------
local matio = require 'matio'

-- load a single array from file
local rawData = matio.load('cnn_features.mat', 'cnn_features')
local rawLabel = matio.load('cnn_labels.mat', 'cnn_labels')

trainData = (rawData:sub(1,para.trainNum)):clone()
testData = (rawData:sub(para.trainNum+1,para.trainNum+para.testNum)):clone()
trainLabel = (rawLabel:sub(1,para.trainNum)):clone()
testLabel = (rawLabel:sub(para.trainNum+1,para.trainNum+para.testNum)):clone()

--trainData.data = matio.load('traindata.mat', 'train_x')
--trainData.label = matio.load('traindata.mat', 'train_y')
--testData.data = matio.load('testdata.mat', 'train_x')
--testData.label = matio.load('testdata.mat', 'train_y')
--validData.data = matio.load('validdata.mat', 'valid_x')
--validData.label = matio.load('validdata.mat', 'valid_y')

----------------------------------------------------------------------
print '==> defining the model'
-- define model
cnn_model()

-- define loss function
cnn_loss()
print '==> here is the loss function:'
print(criterion)

-- this class thing is actually useless, will replace them later
-- classes 15
classes = {'1','2','3','4','5'}

-- This matrix records the current confusion across classes
confusion = optim.ConfusionMatrix(classes)

-- Log results to files
print '==> defining some tools'
trainLogger = optim.Logger(paths.concat(para.savedir, 'train.log'))
testLogger = optim.Logger(paths.concat(para.savedir, 'test.log'))

-- configuring optimizer parameters
optzset()

-- Use CUDA? Of course!
print('==> switching to CUDA')
model:cuda()
criterion:cuda()

----------------------------------------------------------------------
print '==> training!'

for i = 1,50 do
	-- defining training procedure
	train()
	-- defining test procedure
	test()
end

-- save training result and logger
--realOutput = model:forward(testData)
--model = model:double()
--matio.save('cnn1.mat',model)
--matio.save('output1.mat',realOutput)
--matio.save('log1.mat',trainLogger)
-- there might be many other things need to be stored