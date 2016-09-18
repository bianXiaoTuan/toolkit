#!/usr/bin/ruby
# _*_ coding: UTF-8 _*_

# 标准函数定义
def test
    i = 100
    j = 200
    k = 300
    return i, j, k
end

vars = test

vars.each do |var|
    puts var
end

# 可变参数
def sample (*test)
    puts "参数个数为 #{test.length}"

	for i in 0...test.length
	    puts "参数值为 #{test[i]}"
	end
end

sample("Zara", "6", "F")
sample("Mac", "36", "M", "MCA")
