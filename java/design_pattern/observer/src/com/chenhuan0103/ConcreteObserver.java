package com.chenhuan0103;


/**
 * Created by chenhuan on 16/1/5.
 */
public class ConcreteObserver extends Observer{
    @Override
    public void update(String newState) {
        observerState = newState;
        System.out.println("状态为: " + observerState);
    }
}
