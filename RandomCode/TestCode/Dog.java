package TestCode;
public class Dog extends Animal implements Walkable, Speaks{

    public Dog(String name) {
        super(name);
    }
    @Override
    public void walk(){
        System.out.println("Walks on 4 legs on land!");
    }

    @Override
    public void speak(){
        System.out.println("Bark!!");
    }
}