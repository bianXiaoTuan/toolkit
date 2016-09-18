package com.chenhuan0103;

public class Main {
    public static void main(String[] args) {
        Cat cat = new Cat();
        Animal animal = cat;

        if(animal instanceof Cat) {
            Cat cat2 = (Cat)animal;
        } else {
            System.out.println("无法进行类型转换");
        }
    }
}
