package classes;

public class Chapter {
    private String name;
    private String world;

    public Chapter(String name, String world) {
       this.setName(name);
       this.setWorld(world);
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        if(name != null && !name.isEmpty()) {
            this.name = name;
        }else{
            System.out.println("The field cannot be null, the string cannot be empty");
        }
    }

    public String getWorld() {
        return world;
    }

    public void setWorld(String world) {
        if(world != null) {
            this.world = world;
        }else{
            System.out.println("The field cannot be null");
        }
    }
}