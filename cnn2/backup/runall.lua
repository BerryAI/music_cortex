----------------------------------------------------------------------
--This file is used to run all functions in this programme
--for testing use
--
----------------------------------------------------------------------
require 'torch'
require 'cunn'

----------------------------------------------------------------------
print '==> processing options'
print('==> switching to CUDA')

--torch.setdefaulttensortype('torch.FloatTensor')

--threads = 10
--torch.setnumthreads(threads)

seed = 1 --fixed randomization
torch.manualSeed(seed)

----------------------------------------------------------------------
print '==> executing all'

dofile 'cnn_data.lua'
dofile 'cnn_model.lua'
dofile 'cnn_loss.lua'
dofile 'cnn_train.lua'
dofile 'cnn_test.lua'

----------------------------------------------------------------------
print '==> training!'

while true do
   train()
   test()
end