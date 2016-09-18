package com.chenhuan0103;

public class Main {

    public static void main(String[] args) {
        Composite root = new Composite("root");
        root.add(new Leaf("leaf A"));
        root.add(new Leaf("leaf B"));

        Composite comp = new Composite("compA");
        comp.add(new Leaf("leaf C"));
        comp.add(new Leaf("leaf D"));

        root.add(comp);
        root.display(1);
    }
}
