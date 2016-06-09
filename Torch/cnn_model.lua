----------------------------------------------------------------------
--
--
--
--
--
--
--
----------------------------------------------------------------------

require 'cunn'

----------------------------------------------------------------------

function cnn_model()
   local model = nn.Sequential() 
   
   -- convolution layers
   model:add(nn.SpatialConvolutionMM(1, 1, 5, 5, 1, 1))
   model:add(nn.ReLU())
--   model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
   
   model:add(nn.SpatialConvolutionMM(1, 2, 5, 5, 1, 1))
   model:add(nn.ReLU())
--   model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
   
   model:add(nn.SpatialConvolutionMM(256, 512, 4, 4, 1, 1))
   model:add(nn.ReLU())
   
   -- fully connected layers
   model:add(nn.SpatialConvolutionMM(512, 1024, 2, 2, 1, 1))
   model:add(nn.ReLU())
--   model:add(nn.Dropout(0.5))
   model:add(nn.SpatialConvolutionMM(1024, 10, 1, 1, 1, 1))
   
   model:add(nn.Reshape(10))
   model:add(nn.SoftMax())
   
   return model
end

----------------------------------------------------------------------

function cnn_visualize(model)
   print '==> visualizing ConvNet filters'
   print('Layer 1 filters:')
   itorch.image(model:get(1).weight)
   print('Layer 2 filters:')
   itorch.image(model:get(5).weight)
end