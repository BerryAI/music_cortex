----------------------------------------------------------------------
-- This file is used to read .mat file of input training data
--
--
--
--
-- I: nil
-- O: nil
----------------------------------------------------------------------

local matio = require 'matio'

-- load a single array from file
traindata.data = matio.load('traindata.mat', 'train_x')
traindata.label = matio.load('traindata.mat', 'train_y')
testdata.data = matio.load('testdata.mat', 'train_x')
testdata.label = matio.load('testdata.mat', 'train_y')
--validdata.data = matio.load('validdata.mat', 'valid_x')
--validdata.label = matio.load('validdata.mat', 'valid_y')

-- load all arrays from file
--tensors = matio.load('test.mat')