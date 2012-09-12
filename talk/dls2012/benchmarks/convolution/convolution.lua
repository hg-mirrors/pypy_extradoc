module(..., package.seeall);
local ffi = require("ffi")

local function array(length, initializer)
    return ffi.new("double[?]", length, initializer)
end

-- _______________ conv3 _______________

local function _conv3(a, arraylength, k, n)
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

local function conv3(n)
    local arraylength = 100000000/n
    _conv3(array(arraylength, 1), arraylength,
           {-1, 0, 1}, n)
    return string.format("conv3(array(1e%d))", math.log10(100000000/n))
end

-- _______________ conv5 _______________

local function _conv5(a, arraylength, k, n)
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

local function conv5(n)
    local arraylength = 100000000/n
    _conv5(array(arraylength, 1), arraylength,
           {1, 4, 6, 4, 1}, n)
    return string.format("conv5(array(1e%d))", math.log10(100000000/n))
end

-- _______________ conv3x3 _______________

-- begin class Array2D

local mt = { __index = function(o, x) return o.a[x] end }
local tc = {}
local function Array2D(w, h)
  local t = tc[w*2^20+h]
  if not t then
    t = ffi.typeof("struct { int width, height; double a[$][$]; }", w, h)
    tc[w*2^20+h] = t
    ffi.metatype(t, mt)
  end
  return t(w, h)
end

-- end class Array2D

local function _conv3x3(a, b, k)
    assert(k.width == 3 and k.height == 3)
    for y = 1, a.height - 2     do
        for x = 1, a.width - 2 do
            b[x][y] = k[2][2] * a[x-1][y-1] + k[1][2] * a[x][y-1] + k[0][2] * a[x+1][y-1] +
                      k[2][1] * a[x-1][y]   + k[1][1] * a[x][y]   + k[0][1] * a[x+1][y]   +
		      k[2][0] * a[x-1][y+1] + k[1][0] * a[x][y+1] + k[0][0] * a[x+1][y+1]
        end
    end
    return b
end

local function conv3x3(x, y)
    local a = Array2D(x, y)
    local b = Array2D(x, y)
    for i = 1, 10 do
        _conv3x3(a, b, Array2D(3, 3))
    end
    return string.format("conv3x3(Array2D(%dx%d))", x, y)
end


local function morphology3x3(a, b, k, func)
    assert(k.width == 3 and k.height == 3)
    for y = 1, a.height - 2 do
        for x = 1, a.width - 2 do
            b[x][y] = func(k[2][2] * a[x-1][y-1], k[1][2] * a[x][y-1], k[0][2] * a[x+1][y-1],
                           k[2][1] * a[x-1][y],   k[1][1] * a[x][y],   k[0][1] * a[x+1][y],
                           k[2][0] * a[x-1][y+1], k[1][0] * a[x][y+1], k[0][0] * a[x+1][y+1])
        end
    end
    return b
end

local function _dilate3x3(a, b, k)
    return morphology3x3(a, b, k, math.max)
end

local function dilate3x3(x, y)
    local a = Array2D(x, y)
    local b = Array2D(x, y)
    for i = 1, 10 do
        _dilate3x3(a, b, Array2D(3, 3))
    end
    return string.format("dilate3x3(Array2D(%dx%d))", x, y)
end

local function _sobel_magnitude(a)
    local b = Array2D(a.width, a.height)
    for y = 1, a.height - 2 do
        for x = 1, a.width - 2 do
            local dx = -1 * a[x-1][y-1] + 1 * a[x+1][y-1] +
                       -2 * a[x-1][y]   + 2 * a[x+1][y] +
                       -1 * a[x-1][y+1] + 1 * a[x+1][y+1]
            local dy = -1 * a[x-1][y-1] - 2 * a[x][y-1]-1 * a[x+1][y-1] +
                        1 * a[x-1][y+1] + 2 * a[x][y+1]+1 * a[x+1][y+1]
            b[x][y] = math.sqrt(dx * dx + dy * dy) / 4
        end
    end
    return b
end


local function sobel_magnitude(x, y)
    for i = 1, 10 do
        _sobel_magnitude(Array2D(x, y))
    end
    return string.format('sobel(Array2D(%sx%s))', x, y)
end


-- entry point
function main(args)
    local arg = args[1]
    local num = tonumber(args[2]) or 1000
    local num2 = tonumber(args[3]) or num
    if arg == "conv3" then
        return conv3(num)
    elseif arg == "conv5" then
        return conv5(num)
    elseif arg == "conv3x3" then
        return conv3x3(num, num2)
    elseif arg == "dilate3x3" then
        return dilate3x3(num, num2)
    elseif arg == "sobel_magnitude" then
        return sobel_magnitude(num, num2)
    end
end

--main(arg)

