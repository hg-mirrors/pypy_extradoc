local bit = require("bit")
local lshift, rshift, tobit = bit.lshift, bit.rshift, bit.tobit

if true then
    function rshift(a, b)
        return a / (2 ^ b)
    end

    function lshift(a, b)
        return a * (2 ^ b)
    end

    function tobit(a)
        return a
    end
end

---------------------------

function sqrt(y, n)
    n = n or 10000
    local x = y / 2
    while n > 0 do
        n = n - 1
        x = (x + y/x) / 2
    end
    return x
end

-----------------------
-- begin class Fix16 --
-----------------------

Fix16 = {
    new = function(self, val, scale)
        if scale == nil then
            scale = true
        end

        if type(val) == "table" then
            val = val.val
        else
            if scale == true then
                val = lshift(val, 16)
            else
                val = tobit(val)
            end
        end
        return setmetatable({val=val}, self)
    end,

    __add = function(self, other)
        return Fix16:new(self.val + Fix16:new(other).val, false)
    end,

    __mul = function(self, other)
        local value = rshift(self.val, 8) * (rshift(Fix16:new(other).val, 8))
        return Fix16:new(value, false)
    end,

    __div = function(self, other)
        local value = lshift(self.val, 8) / (rshift(Fix16:new(other).val, 8))
        return Fix16:new(value, false)
    end,

    to_float = function(self)
        return self.val / (2 ^ 16)
    end,

    __tostring = function(self)
        return tostring(self:to_float())
    end,
}
Fix16.__index = Fix16

---------------------
-- end class Fix16 --
---------------------

function test_sqrt()
    t = {2, 3, 4, 5, 6, 7, 8, 9, 123}
    for j = 1, #t do
        i = t[j]
        s = string.format("%d %f %f %f %f", i, sqrt(i), sqrt(tobit(i)), sqrt(Fix16:new(i)):to_float(), math.sqrt(i))
        print(s)
    end
end

-- entry point
function main(args)
    arg = args[1]
    if arg == "int" then
        sqrt(123, 100000000)
    elseif arg == "float" then
        sqrt(123, 100000000)
    elseif arg == "Fix16" then
        sqrt(Fix16:new(123), 100000000)
    elseif arg == "test_sqrt" then
        test_sqrt()
    else
        error('argument must be "int", "float" or "Fix16"')
    end
    return string.format("%s", arg)
end

main(arg)
