----------------------------------------------------------------------
--
--
--
--
--
--
--
----------------------------------------------------------------------

require 'torch'   -- torch
require 'xlua'    -- use to display progress bars, not necessary
require 'optim'   -- an optimization package, for online and batch methods

----------------------------------------------------------------------

savedir = '.\'
optimization = 'CG'
ParamaxIter = 50
ParalearningRate = 0.001 
ParaweightDecay = 0
ParastartAveraging = 1
Paramomentum = 0
ParabatchSize = 100
flagplot = false
flagsave = false

----------------------------------------------------------------------
-- Use CUDA? Of course!

model:cuda()
criterion:cuda()

----------------------------------------------------------------------
print '==> defining some tools'

-- Log results to files
trainLogger = optim.Logger(paths.concat(savedir, 'train.log'))
testLogger = optim.Logger(paths.concat(savedir, 'test.log'))

-- Retrieve parameters and gradients:
-- this extracts and flattens all the trainable parameters into a vector
--if model then
--   parameters,gradParameters = model:getParameters()
--end

----------------------------------------------------------------------
print '==> configuring optimizer parameters'

if optimization == 'CG' then
   optimState = {
      maxIter = ParamaxIter
   }
   optimMethod = optim.cg

elseif optimization == 'LBFGS' then
   optimState = {
      learningRate = ParalearningRate,
      maxIter = ParamaxIter,
      nCorrection = 10
   }
   optimMethod = optim.lbfgs

elseif optimization == 'SGD' then
   optimState = {
      learningRate = ParalearningRate,
      weightDecay = ParaweightDecay,
      momentum = Paramomentum,
      learningRateDecay = 1e-7
   }
   optimMethod = optim.sgd

elseif optimization == 'ASGD' then
   optimState = {
      eta0 = ParalearningRate,
      t0 = trsize * ParastartAveraging
   }
   optimMethod = optim.asgd

else
   error('unknown optimization method')
end

----------------------------------------------------------------------
print '==> defining training procedure'

function train()

   -- epoch tracker
   epoch = epoch or 1

   -- local vars
   local time = sys.clock()

   -- set model to training mode
   model:training()

   -- shuffle at each epoch
   shuffle = torch.randperm(trsize)

   -- do one epoch, same as torch tutorial
   print('==> doing epoch on training data:')
   print("==> online epoch # " .. epoch .. ' [batchSize = ' .. ParabatchSize .. ']')
   for t = 1,trainData:size(),ParabatchSize do
      -- disp progress
      xlua.progress(t, trainData:size())

      -- create mini batch
      local inputs = {}
      local targets = {}
      for i = t,math.min(t+ParabatchSize-1,trainData:size()) do
         -- load new sample
         local input = trainData.data[shuffle[i]]
         local target = trainData.labels[shuffle[i]]
         input = input:cuda();
         target = target:cuda()
         table.insert(inputs, input)
         table.insert(targets, target)
      end

      -- create closure to evaluate f(X) and df/dX
      local feval = function(x)
                       -- get new parameters
                       if x ~= parameters then
                          parameters:copy(x)
                       end

                       -- reset gradients
                       gradParameters:zero()

                       -- f is the average of all criterions
                       local f = 0

                       -- evaluate function for complete mini batch
                       for i = 1,#inputs do
                          -- estimate f
                          local output = model:forward(inputs[i])
                          local err = criterion:forward(output, targets[i])
                          f = f + err

                          -- estimate df/dW
                          local df_do = criterion:backward(output, targets[i])
                          model:backward(inputs[i], df_do)

                          -- update confusion
                          confusion:add(output, targets[i])
                       end

                       -- normalize gradients and f(X)
                       gradParameters:div(#inputs)
                       f = f/#inputs

                       -- return f and df/dX
                       return f,gradParameters
                    end

      -- optimize on current mini-batch
      if optimMethod == optim.asgd then
         _,_,average = optimMethod(feval, parameters, optimState)
      else
         optimMethod(feval, parameters, optimState)
      end
   end

   -- time taken
   time = sys.clock() - time
   time = time / trainData:size()
   print("\n==> time to learn 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
   print(confusion)

   -- update logger/plot
   trainLogger:add{['% mean class accuracy (train set)'] = confusion.totalValid * 100}
   if flagplot then
      trainLogger:style{['% mean class accuracy (train set)'] = '-'}
      trainLogger:plot()
   end

   -- save/log current net
   local filename = paths.concat(flagsave, 'model.net')
   os.execute('mkdir -p ' .. sys.dirname(filename))
   print('==> saving model to '..filename)
   torch.save(filename, model)

   -- next epoch
   confusion:zero()
   epoch = epoch + 1
end