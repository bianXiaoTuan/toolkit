package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public class LazySingleton {
    private static LazySingleton instance = null;

    private LazySingleton() {}

    public synchronized static LazySingleton getInstance() {
        if(instance == null) {
            instance = new LazySingleton();
        }
        return instance;
    }
}
