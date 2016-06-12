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

para.savedir = './'
para.optimization = 'CG'
para.maxIter = 50
para.learningRate = 0.001 
para.weightDecay = 0
para.startAveraging = 1
para.momentum = 0
para.batchSize = 100
para.noutputs = 15
para.plot = false
para.save = false

----------------------------------------------------------------------
local matio = require 'matio'

-- load a single array from file
traindata.data = matio.load('traindata.mat', 'train_x')
traindata.label = matio.load('traindata.mat', 'train_y')
testdata.data = matio.load('testdata.mat', 'train_x')
testdata.label = matio.load('testdata.mat', 'train_y')
--validdata.data = matio.load('validdata.mat', 'valid_x')
--validdata.label = matio.load('validdata.mat', 'valid_y')

----------------------------------------------------------------------
print '==> defining the model'
-- define model
model = cnn_model()

-- define loss function
defloss()
print '==> here is the loss function:'
print(criterion)

-- Log results to files
print '==> defining some tools'
trainLogger = optim.Logger(paths.concat(savedir, 'train.log'))
testLogger = optim.Logger(paths.concat(savedir, 'test.log'))

-- Retrieve parameters and gradients:
-- this extracts and flattens all the trainable parameters into a vector
--if model then
--   parameters,gradParameters = model:getParameters()
--end

-- configuring optimizer parameters
optzset()

-- Use CUDA? Of course!
print('==> switching to CUDA')
model:cuda()
criterion:cuda()

----------------------------------------------------------------------
print '==> training!'

while true do
	-- defining training procedure
	train()
	-- defining test procedure
	test()
end

-- save training result and logger
matio.save('cnn1.mat',model)
matio.save('log1.mat',trainLogger)
-- there might be many other things need to be stored