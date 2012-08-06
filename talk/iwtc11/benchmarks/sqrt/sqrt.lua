function sqrt(y, n)
	n = n or 10000
	x = y / 2
	while n > 0 do
		n = n - 1
		x = (x + y/x) / 2
	end
	return x
end

-----------------------
-- begin class Fix16 --
-----------------------

Fix16 = {}
Fix16.__index = Fix16

function Fix16.init(val, scale)
	if scale == nil then
		scale = true
	end

	local fix16 = {}
	setmetatable(fix16, Fix16)
	if type(val) == "table" then
		fix16.val = val.val
	else
		if scale == true then
			fix16.val = math.floor(val * (2 ^ 16))
		else
			fix16.val = val
		end
	end
	return fix16
end

function Fix16:__add(other)
	return Fix16.init(self.val + Fix16.init(other).val, false)
end

function Fix16:__mul(other)
	value = (self.val / 256) * (Fix16.init(other).val / 256)
	return Fix16.init(value, false)
end

function Fix16:__div(other)
	value = (self.val * 256) / (Fix16.init(other).val / 256)
	return Fix16.init(value, false)
end

function Fix16:to_float()
	return self.val / (2 ^ 16)
end

function Fix16:__tostring()
	return tostring(self:to_float())
end

---------------------
-- end class Fix16 --
---------------------

function test_sqrt()
	t = {2, 3, 4, 5, 6, 7, 8, 9, 123}
	for j = 1, #t do
		i = t[j]
		s = string.format("%d %f %4.2f %4.2f %4.2f", i, sqrt(i), sqrt(i), sqrt(Fix16.init(i)):to_float(), math.sqrt(i))
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
		sqrt(Fix16.init(123), 100000000)
	elseif arg == "test_sqrt" then
		test_sqrt()
	else
		error('argument must be "int", "float" or "Fix16"')
	end
	return string.format("%s", arg)
end

--main(arg)
