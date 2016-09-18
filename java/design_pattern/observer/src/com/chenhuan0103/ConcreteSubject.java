package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public class ConcreteSubject extends Subject{
    private String state;

    public void change(String newState) {
        state = newState;
        System.out.println("主题为: " + state);
        this.notify(state);
    }
}
