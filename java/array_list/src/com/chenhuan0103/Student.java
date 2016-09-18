package com.chenhuan0103;

import java.util.Set;
import java.util.HashSet;

/**
 * Created by chenhuan on 16/1/5.
 */
public class Student {
    public String id;
    public String name;
    public Set coures;

    public Student(String id, String name) {
        this.id = id;
        this.name = name;
        this.coures = new HashSet();
    }
}
