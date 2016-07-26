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
   model:add(nn.SpatialConvolution(1, 4, 4, 9))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(4, 4, 4, 4))
   
   model:add(nn.SpatialConvolution(4, 8, 4, 5))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
   
   model:add(nn.SpatialConvolution(8, 16, 4, 4))
   model:add(nn.ReLU())
   model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
   
   model:add(nn.SpatialConvolution(16, 16, 4, 5))
   model:add(nn.ReLU())
   -- fully connected layers
--   model:add(nn.Dropout(0.5))
   outsize = model:outside{3,1,128,999} -- output size of convolutions
   model:add(nn.Collapse(3))
   model:add(nn.Linear(outsize[2]*outsize[3]*outsize[4], 128))
   
   model:add(nn.Linear(128,64))
   
   model:add(nn.Linear(64,5))
--   model:add(nn.SoftMax())
   
--   return model
end
