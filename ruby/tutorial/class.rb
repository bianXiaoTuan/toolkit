#!/usr/bin/ruby
# _*_ coding: UTF-8 _*_

=begin
ruby类中变量
1. 局部变量: _开头, 私有数据成员
2. 实例变量: @开头, 共有数据成员
3. 类变量: @@开头, 静态数据成员
4. 全局变量: $开头
=end


class Customer
    @@no_of_customers = 0

	def initialize(id, name, addr)
	    @cust_id = id
		@cust_name = name
		@cust_addr = addr

        @@no_of_customers += 1
    end

    def display_details()
        puts "Customer id #@cust_id"
        puts "Customer name #@cust_name"
        puts "Customer address #@cust_addr"
    end

    def total_no_of_customers()
        puts "Total number of customers: #@@no_of_customers"
    end

	def print_name
	    puts "name: %s" % @cust_name
	end
end

cust1 = Customer.new(1, '陈欢', '北京')
cust2 = Customer.new(2, '姜虹', '杭州')

cust1.display_details()
cust2.display_details()

cust1.total_no_of_customers()
cust2.total_no_of_customers()
