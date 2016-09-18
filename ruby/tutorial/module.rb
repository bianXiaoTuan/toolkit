#!/usr/bin/ruby
# _*_ coding: UTF-8 _*_

# 定义在 module.rb 文件中的模块
module Trig
    PI = 3.141592654

    def Trig.sin(x)
        # ..
    end

    def Trig.cos(x)
        # ..
    end
end

# require语句
$LOAD_PATH << '.'

require 'trig.rb'
require 'moral'

y = Trig.sin(Trig::PI/4)
wrongdoing = Moral.sin(Moral::VERY_BAD)

# include语句
$LOAD_PATH << '.'
require "support"

class Decade
    include Week
    no_of_yrs=10

    def no_of_months
       puts Week::FIRST_DAY
       number=10*12
       puts number
    end
end

d1=Decade.new
puts Week::FIRST_DAY
Week.weeks_in_month
Week.weeks_in_year
d1.no_of_months

