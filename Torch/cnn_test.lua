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
   print('==> testing on test set:')
   for t = 1,testData:size() do
      -- disp progress
      xlua.progress(t, testData:size())

      -- get new sample
      local input = testData.data[t]
      input = input:cuda()
      local target = testData.labels[t]

      -- test sample
      local pred = model:forward(input)
      confusion:add(pred, target)
   end

   -- timing
   time = sys.clock() - time
   time = time / testData:size()
   print("\n==> time to test 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
   print(confusion)

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
end