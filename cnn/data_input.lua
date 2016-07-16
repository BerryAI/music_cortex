----------------------------------------------------------------------
-- This function is used to fast read file in to a Tensor
-- Really very fast
-- This is a by-product cuz i find it useless against txt written numbers
-- I: <string>file path
-- O: <tensor>data Tensor
----------------------------------------------------------------------
local ffi = require 'ffi'
-- this function loads a file line by line to avoid having memory issues
function lf2t(path) --load_file_to_tensor
    -- intialize tensor for the file
    local file_tensor = torch.CharTensor() --torch.CharTensor() for characters
    
    --[[ get  number of rows/collumns ]]
    local file = io.open(path, 'r') -- open file
    local max_line_size = 0
    local number_of_lines = 0
    for line in file:lines() do
        -- get maximum line size
        max_line_size = math.max(max_line_size, #line +1) -- the +1 is important to correctly fetch data
        
        -- increment the number of lines counter
        number_of_lines = number_of_lines +1
    end
    file:close() --close file
    
    -- Now that we have the maximum size of the vector, we just have to allocat memory for it (as long there is enough memory in ram)
    file_tensor = file_tensor:resize(number_of_lines, max_line_size):fill(0)
    local f_data = file_tensor:data()
    
    -- The only thing left to do is to fetch data into the tensor. 
    -- Lets open the file again and fill the tensor using ffi
    local file = io.open(path, 'r') -- open file
    for line in file:lines() do
        -- copy data into the tensor line by line
        ffi.copy(f_data, line)
        f_data = f_data + max_line_size
    end
    file:close() --close file
    
    return file_tensor
end
----------------------------------------------------------------------
-- This function is used to convert text file into byte Tensor
-- 
-- This is a by-product cuz i find it useless against txt written numbers
-- I: <string>infile path, outfile path
-- O: nil
----------------------------------------------------------------------
function t2t(in_textfile, out_vocabfile, out_tensorfile) --text_to_tensor
    local timer = torch.Timer()

    print('loading text file...')
    local cache_len = 10000
    local rawdata
    local tot_len = 0
    local f = assert(io.open(in_textfile, "r"))

    -- create vocabulary if it doesn't exist yet
    print('creating vocabulary mapping...')
    -- record all characters to a set
    local unordered = {}
    rawdata = f:read(cache_len)
    repeat
        for char in rawdata:gmatch'.' do
            if not unordered[char] then unordered[char] = true end
        end
        tot_len = tot_len + #rawdata
        rawdata = f:read(cache_len)
    until not rawdata
    f:close()
    -- sort into a table (i.e. keys become 1..N)
    local ordered = {}
    for char in pairs(unordered) do ordered[#ordered + 1] = char end
    table.sort(ordered)
    -- invert `ordered` to create the char->int mapping
    local vocab_mapping = {}
    for i, char in ipairs(ordered) do
        vocab_mapping[char] = i
    end
    -- construct a tensor with all the data
    print('putting data into tensor...')
    local data = torch.ByteTensor(tot_len) -- store it into 1D first, then rearrange
    f = assert(io.open(in_textfile, "r"))
    local currlen = 0
    rawdata = f:read(cache_len)
    repeat
        for i=1, #rawdata do
            data[currlen+i] = vocab_mapping[rawdata:sub(i, i)] -- lua has no string indexing using []
        end
        currlen = currlen + #rawdata
        rawdata = f:read(cache_len)
    until not rawdata
    f:close()

    -- save output preprocessed files
    print('saving ' .. out_tensorfile)
    torch.save(out_tensorfile, data)
end
----------------------------------------------------------------------
-- This function is used to convert text file into num Tensor
-- 
-- This is a by-product cuz i find it useless against txt written numbers
-- I: <string>file path
-- O: <tensor>data Tensor
----------------------------------------------------------------------
function string:splitAtCommas()
  local sep, values = ",", {}
  local pattern = string.format("([^%s]+)", sep)
  self:gsub(pattern, function(c) values[#values+1] = c end)
  return values
end

function loadData(dataFile)
  local dataset = {}
  local i = 1
  for line in io.lines(dataFile) do
    local values = line:splitAtCommas()
    local y = torch.Tensor(1)
    y[1] = values[#values] -- the target class is the last number in the line
    values[#values] = nil
    local x = torch.Tensor(values) -- the input data is all the other numbers
    dataset[i] = torch.Tensor(values)
    i = i + 1
  end
  function dataset:size() return (i - 1) end -- the requirement mentioned
  return dataset
end