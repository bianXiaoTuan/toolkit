package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public class Singleton {
    private static Singleton instance = new Singleton();

    private Singleton() {}

    public synchronized static Singleton getInstance() {
        return instance;
    }
}
