module(..., package.seeall);

local ffi = require("ffi")
local bit = require("bit")
local lshift, rshift = bit.lshift, bit.rshift

---------------------------

local function sqrt(y, n)
  local x = y / 2
  for n=n or 10000,0,-1 do x = (x + y/x) / 2 end
  return x
end

-----------------------
-- begin class Fix16 --
-----------------------

local Fix16 = ffi.typeof("struct { int val; }")
local new, istype = ffi.new, ffi.istype

ffi.metatype(Fix16, {
  __new = function(t, a)
    if istype(Fix16, a) then return a end
    return new(Fix16, lshift(a, 16))
  end,
  __add = function(a, b)
    return new(Fix16, Fix16(a).val + Fix16(b).val)
  end,
  __div = function(a, b)
    return new(Fix16, lshift(Fix16(a).val, 8) / rshift(Fix16(b).val, 8))
  end,
  __index = {
    to_float = function(a) return a.val / 2^16 end,
  },
})

---------------------
-- end class Fix16 --
---------------------

local function test_sqrt()
    local t = {2, 3, 4, 5, 6, 7, 8, 9, 123}
    for j = 1, #t do
        local i = t[j]
        local s = string.format("%d %f %f %f %f", i, sqrt(i), sqrt(i), sqrt(Fix16(i)):to_float(), math.sqrt(i))
        print(s)
    end
end

-- entry point
function main(args)
    local arg = args[1]
    if arg == "int" then
        sqrt(123, 100000000)
    elseif arg == "float" then
        sqrt(123, 100000000)
    elseif arg == "Fix16" then
        sqrt(Fix16(123), 100000000)
    elseif arg == "test_sqrt" then
        test_sqrt()
    else
        error('argument must be "int", "float" or "Fix16"')
    end
    return string.format("%s", arg)
end

--main(arg)
