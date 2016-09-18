package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
	// write your code here
        Main main = new Main();
        try {
            main.test2();
        } catch(Exception e) {
            e.printStackTrace();
        }
    }

    public void test1() throws DrunkException{
        throw new DrunkException("开车别喝酒");
    }

    public void test2() {
        try {
            test1();
        } catch(DrunkException e) {
            RuntimeException newExp = new RuntimeException("司机一滴酒, 亲人两行泪");
            newExp.initCause(e);
            throw newExp;
        }
    }
}
