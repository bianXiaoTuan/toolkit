package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/4.
 */
public class Dog extends Animal{
    public int age = 20;

    public Dog() {
    }

    public void eat() {
        System.out.println("Dog eating");
    }

    public void method() {
        System.out.println(super.age);
    }

    @Override
    public String toString() {
        return "Dog{" +
                "age=" + age +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Dog)) return false;

        Dog dog = (Dog) o;
        return age == dog.age;
    }

    @Override
    public int hashCode() {
        return age;
    }
}
