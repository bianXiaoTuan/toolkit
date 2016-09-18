package com.chenhuan0103;

/**
 * Created by chenhuan on 16/1/5.
 */
public class Leaf extends Component{
    public Leaf(String name) {
        super(name);
    }

    public void add(Component c) {
        System.out.println("Leaf不能新增子节点");
    }

    public void remove(Component c) {
        System.out.println("Leaf不能删除子节点");
    }

    public void display(int depth) {
        for(int i=0 ; i<depth-1 ; i++) {
            System.out.print('-');
        }
        System.out.println(this.name);
    }
}
