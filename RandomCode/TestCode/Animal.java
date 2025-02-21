package TestCode;
public class Animal{
    private String name = "";
    public Animal(String name) {
        this.name = name;
    }

    public void getName(){
        System.err.println("My name is: " + this.name);
    }
}