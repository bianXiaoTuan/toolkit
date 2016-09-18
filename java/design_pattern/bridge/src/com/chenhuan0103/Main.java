package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
        Red red = new Red();
        Green green = new Green();

        BigBrush bb = new BigBrush();
        bb.setColor(red);
        bb.paint();
        bb.setColor(green);
        bb.paint();

        SmallBrush sb = new SmallBrush();
        sb.setColor(red);
        sb.paint();
        sb.setColor(green);
        sb.paint();
    }
}
