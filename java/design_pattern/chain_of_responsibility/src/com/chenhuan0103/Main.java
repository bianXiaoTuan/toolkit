package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
        ConcreteHandler ch1 = new ConcreteHandler("ch1");
        ConcreteHandler ch2 = new ConcreteHandler("ch2");
        ConcreteHandler ch3 = new ConcreteHandler("ch3");

        ch1.setSuccessor(ch2);
        ch2.setSuccessor(ch3);

        ch1.handleRequest();
    }
}
