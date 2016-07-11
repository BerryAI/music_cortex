----------------------------------------------------------------------
-- This file defines the model of CNN
--
-- I: nil
-- O: nil
----------------------------------------------------------------------

require 'nn'
require 'cunn'
require 'dp'

----------------------------------------------------------------------

function cnn_model()
   model = nn.Sequential() 
   -- convolution layers
   model:add(nn.SpatialConvolution(2, 10, 5, 5))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(1, 2, 1, 2))
   
   model:add(nn.SpatialConvolution(10, 10, 5, 5))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(1, 2, 1, 2))
   
   model:add(nn.SpatialConvolution(10, 20, 4, 5))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(1, 2, 1, 2))
   
   -- fully connected layers
--   model:add(nn.Dropout(0.5))
   outsize = model:outside{3,2,100,12} -- output size of convolutions
   model:add(nn.Collapse(3))
   model:add(nn.Linear(outsize[2]*outsize[3]*outsize[4], 64))

   model:add(nn.Linear(64,128))
   
   model:add(nn.Linear(128,128))
   
   model:add(nn.Linear(128,15))
   model:add(nn.SoftMax())
   
--   return model
end

----------------------------------------------------------------------

function cnn_visualize(model)
   print '==> visualizing ConvNet filters'
   print('Layer 1 filters:')
   itorch.image(model:get(1).weight)
   print('Layer 2 filters:')
   itorch.image(model:get(5).weight)
end