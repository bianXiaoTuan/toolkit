package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public abstract class Handler {

    protected String name;
    protected Handler successor;

    public Handler(String name) {
        this.name = name;
    }

    public abstract void handleRequest();

     public Handler getSuccessor() {
        return successor;
    }

    public void setSuccessor(Handler successor) {
        this.successor = successor;
    }
}
