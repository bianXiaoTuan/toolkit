package com.chenhuan0103;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by chenhuan on 16/1/5.
 */
public class Composite extends Component{
    private List<Component> children;

    public Composite(String name) {
        super(name);
        children = new ArrayList<Component>();
    }

    public void add(Component c) {
        children.add(c);
    }

    public void remove(Component c) {
        children.remove(c);
    }

    public void display(int depth) {
        for(int i=0 ; i < depth-1 ; i++) {
            System.out.print('-');
        }
        System.out.println(this.name);

        for(Component child : children) {
            child.display(depth+2);
        }
    }
}
