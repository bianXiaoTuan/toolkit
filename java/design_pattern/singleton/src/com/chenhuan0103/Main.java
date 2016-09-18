package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
        Singleton obj1 = Singleton.getInstance();
        System.out.println(obj1);

        Singleton obj2 = Singleton.getInstance();
        System.out.println(obj2);
    }
}
