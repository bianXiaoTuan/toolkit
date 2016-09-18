package com.chenhuan0103;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class ListTest {
    public List courseToSelect;

    public ListTest() {
        this.courseToSelect = new ArrayList();
    }

    public void add() {
        Course cr1 = new Course("1", "数据结构");
        courseToSelect.add(cr1);

        Course cr2 = new Course("2", "C语言");
        courseToSelect.add(0, cr2);

        Course[] courses = {new Course("4", "数学"), new Course("5", "语文")};
        courseToSelect.addAll(Arrays.asList(courses));

        Course[] courses2 = {new Course("5", "数学"), new Course("6", "语文")};
        courseToSelect.addAll(0, Arrays.asList(courses2));
    }

    public void get() {
        int length = courseToSelect.size();
        for(int i=0 ; i<length ; i++) {
            Course cr = (Course)courseToSelect.get(i);
            System.out.println("课程: " + cr.name);
        }
    }

    public void testIterator() {
        Iterator it = courseToSelect.iterator();
        while(it.hasNext()) {
            Course cr = (Course)it.next();
            System.out.println("课程: " + cr.id);
        }
    }

    public void testModify() {
        courseToSelect.set(0, new Course("0", "毛概"));
        Course cr = (Course)courseToSelect.get(0);
        System.out.println("课程: " + cr.name);

    }

    public void testRemove() {
        courseToSelect.remove(0);

        Course cr = (Course)courseToSelect.get(0);
        courseToSelect.remove(cr);

        Course[] courses = {(Course) courseToSelect.get(0), (Course) courseToSelect.get(1)};
        courseToSelect.removeAll(Arrays.asList(courses));
    }

    public static void main(String[] args) {
        ListTest lt = new ListTest();
        lt.add();
        lt.testIterator();
        lt.testModify();
        lt.testRemove();
        lt.get();
    }
}
