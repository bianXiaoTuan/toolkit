#!/usr/bin/ruby
# -*- coding: UTF-8 -*-

# while..end
$i = 0
$num = 5
while $i < $num  do
   puts("在循环语句中 i = #$i" )
   $i +=1
end

# begin..end while
$i = 0
$num = 5
begin
   puts("在循环语句中 i = #$i" )
   $i +=1
end while $i < $num

# utils..end
$i = 0
$num = 5

until $i > $num  do
   puts("在循环语句中 i = #$i" )
   $i +=1;
end

# begin..end util
$i = 0
$num = 5
begin
   puts("在循环语句中 i = #$i" )
   $i +=1;
end until $i > $num

# for
for i in 0..5
    puts "局部变量的值为 #{i}"
end

# for遍历数组
arr = [1, 2, 3, 4, 5, 6]
arr.each do |a|
    print a, ''
end

# break
for i in 0..5
	if i > 2 then
	    break
	end
	puts "局部变量的值为 #{i}"
end

# next
for i in 0..5
	if i < 2 then
	    next
	end
	puts "局部变量的值为 #{i}"
end

