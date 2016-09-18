package com.chenhuan0103;
import com.chenhuan0102.TelPhone;

public class Main {

    public static void main(String[] args) {
	// write your code here
        TelPhone phone = new TelPhone(1.0f, 1.0f, 64f);
        phone.setMem(128.0f);

        phone.printTelPhoneCount();
        phone.message();
    }
}
