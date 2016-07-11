----------------------------------------------------------------------
-- loss functions:
--   + negative-log likelihood, using log-normalized output units (SoftMax)
--   + mean-square error
--   + margin loss (SVM-like)
--
--
----------------------------------------------------------------------

require 'torch'   -- torch
require 'nn'      -- provides all sorts of loss functions

----------------------------------------------------------------------
-- 10-class problem, 10 for now at least
noutputs = 10

----------------------------------------------------------------------
print '==> define loss'

if para.loss == 'margin' then

   -- It is an SVM-like loss with a default margin of 1.
   criterion = nn.MultiMarginCriterion()

elseif para.loss == 'nll' then

   -- This loss requires properly normalized log-probabilities
   model:add(nn.LogSoftMax())
   criterion = nn.ClassNLLCriterion()

elseif para.loss == 'mse' then

   -- for MSE, tanh is needed to restrict the model's output
   model:add(nn.Tanh())

   criterion = nn.MSECriterion()
   criterion.sizeAverage = false

   if trainData then
      -- convert training labels:
      local trsize = (#trainData.labels)[1]
      local trlabels = torch.Tensor( trsize, noutputs )
      trlabels:fill(-1)
      for i = 1,trsize do
         trlabels[{ i,trainData.labels[i] }] = 1
      end
      trainData.labels = trlabels

      -- convert test labels
      local tesize = (#testData.labels)[1]
      local telabels = torch.Tensor( tesize, noutputs )
      telabels:fill(-1)
      for i = 1,tesize do
         telabels[{ i,testData.labels[i] }] = 1
      end
      testData.labels = telabels
   end

else

   error('unknown -loss')

end

----------------------------------------------------------------------
print '==> here is the loss function:'
print(criterion)