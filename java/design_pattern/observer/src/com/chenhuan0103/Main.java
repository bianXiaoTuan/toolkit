package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
        ConcreteSubject subject = new ConcreteSubject();

        ConcreteObserver observer1 = new ConcreteObserver();
        ConcreteObserver observer2 = new ConcreteObserver();
        ConcreteObserver observer3 = new ConcreteObserver();
        ConcreteObserver observer4 = new ConcreteObserver();
        ConcreteObserver observer5 = new ConcreteObserver();
        ConcreteObserver observer6 = new ConcreteObserver();

        subject.attach(observer1);
        subject.attach(observer2);
        subject.attach(observer3);
        subject.attach(observer4);
        subject.attach(observer5);
        subject.attach(observer6);

        subject.change("state_A");
        subject.change("state_B");
    }
}
