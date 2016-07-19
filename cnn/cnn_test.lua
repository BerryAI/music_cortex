----------------------------------------------------------------------
-- This function defines the testing procedure
-- and the log procedure
--
-- I: nil
-- O: nil
----------------------------------------------------------------------

require 'torch'   -- torch
require 'xlua'    -- use to display progress bars, not necessary
require 'optim'   -- an optimization package, for online and batch methods

----------------------------------------------------------------------
--print '==> defining test procedure'
--
-- test function
function test()
   -- local vars
   local time = sys.clock()

   -- averaged param use?
   if para.average then
      cachedparams = parameters:clone()
      parameters:copy(para.average)
   end

   -- set model to evaluate mode
   model:evaluate()

   -- test over test data
   local lossAvg = 0
   print('==> testing on test set:')
   for t = 1,para.testNum do
      -- disp progress
      xlua.progress(t, para.testNum)

      -- get new sample
      local input = testData[t]
      input = input:cuda()
      local target = testLabel[t]

      -- test sample
      local pred = model:forward(input)
      confusion:add(pred, target)
      local lossDif = pred-target:cuda()
      lossAvg = lossAvg+torch.dot(lossDif,lossDif)
   end

   -- timing
   time = sys.clock() - time
   time = time / para.testNum
   print("\n==> time to test 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
--   print(confusion)
   lossAvg = (lossAvg/para.testNum)/5 --5 classes
   print("\n==> Loss = " .. lossAvg)

   -- update log/plot
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
   if para.plot then
      testLogger:style{['% mean class accuracy (test set)'] = '-'}
      testLogger:plot()
   end

   -- averaged param use?
   if para.average then
      -- restore parameters
      parameters:copy(cachedparams)
   end
   
   -- next iteration:
   confusion:zero()
   return lossAvg
end