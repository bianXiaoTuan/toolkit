#!/usr/bin/ruby
# _*_ coding: UTF-8 _*_

# 块基本用法
def test
    puts "在 test 方法内"
    yield
    puts "你又回到了 test 方法内"
    yield
end
test {puts "你在块内"}

def test
   yield 5
   puts "在 test 方法内"
   yield 100
   end
test {|i| puts "你在块 #{i} 内"}

# BEGIN 和 END
BEGIN { 
    # BEGIN 代码块
    puts "BEGIN 代码块"
} 

END { 
    # END 代码块
    puts "END 代码块"
}

# MAIN 代码块
puts "MAIN 代码块"
