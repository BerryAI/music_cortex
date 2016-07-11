----------------------------------------------------------------------
-- This file is used to store the 
--
-- I: nil
-- O: nil
----------------------------------------------------------------------

local matio = require 'matio'

matio.save('cnn1.mat',model)
matio.save('log1.mat',trainLogger)

-- there might be many other things need to be stored