----------------------------------------------------------------------
-- loss functions:
--   + negative-log likelihood, using log-normalized output units (SoftMax)
--   + mean-square error
--   + margin loss (SVM-like)
--
-- I: nil
-- O: nil
----------------------------------------------------------------------

require 'torch'   -- torch
require 'nn'      -- provides all sorts of loss functions

----------------------------------------------------------------------
function cnn_loss()
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

	else
	
		error('unknown -loss')
		
	end
end