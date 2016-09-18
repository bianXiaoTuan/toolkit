package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public class ConcreteHandler extends Handler{

    public ConcreteHandler(String name) {
        super(name);
    }

    public void handleRequest() {
        if(getSuccessor() != null) {
            System.out.println(name + "放过请求");
            getSuccessor().handleRequest();
        } else {
            System.out.println(name + "处理请求");
        }
    }
}
