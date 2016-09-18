package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public abstract class Brush {
    protected Color color;

    public abstract void paint();

    public void setColor(Color color) {
        this.color = color;
    }

}
