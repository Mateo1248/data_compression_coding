package com.company;


import java.util.Map;
import java.util.TreeMap;

public class Predecessors  {
    private Map<Byte, Double> predecessors;

    private Predecessors(){}

    public Predecessors(Map<Byte, Double> bs) {
        predecessors = new TreeMap<>();
        for(Byte b : bs.keySet()) {
            predecessors.put(b, 0.0);
        }
    }

    public Map<Byte, Double> getMap() {
        return predecessors;
    }

    public void incEl(Byte b) {
        predecessors.replace(b, predecessors.get(b)+1);
    }
}
