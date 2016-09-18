package com.company;

/**
 * Created by chenhuan on 16/1/4.
 */
public class SmartPhone extends Telphone implements IPlayGame {
    @Override
    public void call() {
        System.out.println("通过语音打电话");
    }

    @Override
    public void message() {
        System.out.println("通过语音发短信");
    }

    @Override
    public void playGame() {
        System.out.println("具备玩游戏功能");
    }
}
