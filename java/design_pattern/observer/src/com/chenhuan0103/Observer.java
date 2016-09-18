package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public abstract class Observer {
   protected String observerState;

   public abstract void update(String newState);
}
