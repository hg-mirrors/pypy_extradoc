module(..., package.seeall);
local ffi = require("ffi")

function array(length, initializer)
    return ffi.new("double[?]", length, initializer)
end

-- _______________ conv3 _______________

function _conv3(a, arraylength, k, n)
    assert(#k == 3)
    local b = array(arraylength - 2, 0)
    while n > 0 do
        n = n - 1
        -- b needs zero-based indexing, k 1-based indexing
        for i = 0, arraylength - 3 do
            b[i] = k[3] * a[i] + k[2] * a[i + 1] + k[1] * a[i + 2]
        end
    end
    return b
end

function conv3(n)
    local arraylength = 100000000/n
    _conv3(array(arraylength, 1), arraylength,
           {-1, 0, 1}, n)
    return string.format("conv3(array(1e%d))", math.log10(100000000/n))
end

-- _______________ conv5 _______________

function _conv5(a, arraylength, k, n)
    assert(#k == 5)
    n = n or 1
    local b = array(arraylength - 4, 0)
    while n > 0 do
        n = n - 1
        -- b needs zero-based indexing, k 1-based indexing
        for i = 0, arraylength - 5 do
            b[i] = k[5]*a[i] + k[4]*a[i+1] + k[3]*a[i+2] + k[2]*a[i+3] + k[1]*a[i+4]
        end
    end
    return b
end

function conv5(n)
    local arraylength = 100000000/n
    _conv5(array(arraylength, 1), arraylength,
           {1, 4, 6, 4, 1}, n)
    return string.format("conv5(array(1e%d))", math.log10(100000000/n))
end

-- _______________ conv3x3 _______________

-- begin class Array2D

Array2D = {

    new = function(self, w, h, initializer)
        initializer = initializer or 0
        return setmetatable(
            {width = w, height = h, data=array(w * h, initializer)}, self)
    end,

    __tostring = function(self)
        return string.format("Array2D(%d, %d)", self.width, self.height)
    end,

    idx = function(self, x, y)
        return y * self.width + x
    end,

    get = function(self, x, y)
        return self.data[self:idx(x, y)]
    end,

    set = function(self, x, y, val)
        self.data[self:idx(x, y)] = val
    end,
}

Array2D.__index = Array2D

-- end class Array2D

function _conv3x3(a, b, k)
    assert(k.width == 3 and k.height == 3)
    for y = 1, a.height - 2     do
        for x = 1, a.width - 2 do
            b:set(x, y, k:get(2, 2) * a:get(x - 1, y - 1) + k:get(1, 2) * a:get(x, y - 1) + k:get(0, 2) * a:get(x + 1, y - 1) +
                        k:get(2, 1) * a:get(x - 1, y) + k:get(1, 1) * a:get(x, y) + k:get(0, 1) * a:get(x + 1, y) +
                        k:get(2, 0) * a:get(x - 1, y + 1) + k:get(1, 0) * a:get(x, y + 1) + k:get(0, 0) * a:get(x + 1, y + 1))
        end
    end
    return b
end

function conv3x3(x, y)
    local a = Array2D:new(x, y)
    local b = Array2D:new(x, y)
    for i = 1, 10 do
        _conv3x3(a, b, Array2D:new(3, 3))
    end
    return string.format("conv3x3(Array2D(%dx%d))", x, y)
end


function morphology3x3(a, b, k, func)
    assert(k.width == 3 and k.height == 3)
    for y = 1, a.height - 2 do
        for x = 1, a.width - 2 do
            b:set(x, y, func(k:get(2, 2) * a:get(x - 1, y - 1), k:get(1, 2) * a:get(x, y - 1), k:get(0, 2) * a:get(x + 1, y - 1),
                             k:get(2, 1) * a:get(x - 1, y), k:get(1, 1) * a:get(x, y), k:get(0, 1) * a:get(x + 1, y),
                             k:get(2, 0) * a:get(x - 1, y + 1), k:get(1, 0) * a:get(x, y + 1), k:get(0, 0) * a:get(x + 1, y + 1)))
        end
    end
    return b
end

function _dilate3x3(a, b, k)
    return morphology3x3(a, b, k, math.max)
end

function dilate3x3(x, y)
    local a = Array2D:new(x, y)
    local b = Array2D:new(x, y)
    for i = 1, 10 do
        _dilate3x3(a, b, Array2D:new(3, 3))
    end
    return string.format("dilate3x3(Array2D(%dx%d))", x, y)
end

function _sobel_magnitude(a)
    b = Array2D:new(a.width, a.height)
    for y = 1, a.height - 2 do
        for x = 1, a.width - 2 do
            local dx = -1 * a:get(x - 1, y - 1) + 1 * a:get(x + 1, y - 1) +
                       -2 * a:get(x - 1, y) + 2 * a:get(x + 1, y) +
                       -1 * a:get(x - 1, y + 1) + 1 * a:get(x + 1, y + 1)
            local dy = -1 * a:get(x - 1, y - 1) - 2 * a:get(x, y - 1) - 1 * a:get(x + 1, y - 1) +
                        1 * a:get(x - 1, y + 1) + 2 * a:get(x, y + 1) + 1 * a:get(x + 1, y + 1)
            b:set(x, y, math.sqrt(dx * dx + dy * dy) / 4)
        end
    end
    return b
end


function sobel_magnitude(x, y)
    for i = 1, 10 do
        _sobel_magnitude(Array2D:new(x, y))
    end
    return string.format('sobel(Array2D(%sx%s))', x, y)
end


-- entry point
function main(args)
    arg = args[1]
    num = tonumber(args[2])
    if arg == "conv3" then
        return conv3(num)
    elseif arg == "conv5" then
        return conv5(num)
    elseif arg == "conv3x3" then
        num2 = tonumber(args[3])
        return conv3x3(num, num2)
    elseif arg == "dilate3x3" then
        num2 = tonumber(args[3])
        return dilate3x3(num, num2)
    elseif arg == "sobel_magnitude" then
        num2 = tonumber(args[3])
        return sobel_magnitude(num, num2)
    end
end

--main(arg)

