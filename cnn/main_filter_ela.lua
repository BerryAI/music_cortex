require 'torch'
require 'cutorch'
require 'nn'
require 'cunn'
require 'dp'
require 'os'
model = torch.load('log/cnn160801172442.dat')
for i = 1,14 do
	model:remove(17-i)
end
model:add(nn.Sum(4))

para = {savedir = "log/",
		batchSize = 25, --100
		plot = false,
		save = false}

----------------------------------------------------------------------
local matio = require 'matio'

-- load a single array from file
local rawData = matio.load('cnn_features.mat', 'cnn_features')

testData = rawData:clone()
model:cuda()
model:evaluate()
realOutput = model:forward(testData:cuda())

realOutput = realOutput:double()
tlabel = os.date("%y%m%d%H%M%S")
matio.save(para.savedir..'filter'..tlabel..'.mat',realOutput)