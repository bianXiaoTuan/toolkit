package com.chenhuan0103;


import java.util.ArrayList;
import java.util.List;

/**
 * Created by chenhuan on 16/1/5.
 */
public abstract class Subject {
    private List<Observer> list = new ArrayList<Observer>();

    public void attach(Observer observer) {
        list.add(observer);
    }

    public void detach(Observer observer) {
        list.remove(observer);
    }

    public void notify(String newState) {
        for(Observer observer : list) {
            observer.update(newState);
        }
    }
}
