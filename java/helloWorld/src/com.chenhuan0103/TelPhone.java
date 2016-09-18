package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/4.
 */
public class TelPhone {
    // 属性(成员变量)
    private float screen;
    private float cpu;
    private float mem;
    static public int count = 0;

    public float getScreen() {
        return screen;
    }

    public void setScreen(float screen) {
        this.screen = screen;
    }

    public float getCpu() {
        return cpu;
    }

    public void setCpu(float cpu) {
        this.cpu = cpu;
    }

    public float getMem() {
        return mem;
    }

    public void setMem(float mem) {
        this.mem = mem;
    }

    // 构造函数
    public TelPhone() {
        TelPhone.count += 1;
    }

    public TelPhone(float newScreen, float newCpu, float newMem) {
        TelPhone.count += 1;
        screen = newScreen;
        cpu = newCpu;
        mem = newMem;
    }

    // 静态函数
    static public void printTelPhoneCount() {
        System.out.println("已经有"+TelPhone.count+"个手机");
    }

    // 公共函数
    public void message() {
        System.out.println("在com.chenhuan0103.com中");
    }
}
