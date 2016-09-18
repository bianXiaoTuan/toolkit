package com.company;

public class Main {

    public static void main(String[] args) {
        Telphone phone1 = new CellPhone();
        Telphone phone2 = new SmartPhone();

        phone1.call();
        phone1.message();

        phone2.call();
        phone2.message();

        SmartPhone phone3 = new SmartPhone();
        phone3.playGame();

        IPlayGame ip3 = new IPlayGame() {
            @Override
            public void playGame() {
                System.out.println("使用匿名内部类方式实现接口");
            }
        };
        ip3.playGame();
    }
}
