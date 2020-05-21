package com.company;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.*;

public class Enthropy {

    private String filePath;
    private byte[] bytes;
    private Double allBytes;
    private Map<Byte, Double> countBytes;
    private Map<Byte, Predecessors> countCondBytes;

    Enthropy(String filePath) {
        this.filePath = filePath;
        this.bytes = getBytes();
        this.allBytes = (double)bytes.length;
    }

    public void result() {
        countBytes();
        double x = enthropy();
        countCondBytes();
        double y = condEnthropy();
        System.out.println("entropia: "+ x);
        System.out.println("entropia warunkowa: "+ y);
        System.out.println("(entropia) - (entropia warunkowa) = " + (x-y));
    }

    public double enthropy() {
        double enthropy = 0;
        for(Double quantity : countBytes.values()) {
            double probability = (double)quantity / allBytes;
            enthropy +=  probability * log2(probability);
        }
        return Math.abs(enthropy);
    }

    private byte[] getBytes() {
        byte[] bytes = null;
        try {
            bytes = Files.readAllBytes(Paths.get(filePath));
        }
        catch(IOException e) {
            System.err.println("Nie można przeczytać pliku!");
            e.printStackTrace();
        }
        return bytes;
    }

    private void countBytes() {
        countBytes = new TreeMap<>();
        for(byte b : bytes) {
            if(countBytes.containsKey(b)) {
                countBytes.replace(b, countBytes.get(b)+1);
            }
            else {
                countBytes.put(b, 1.0 );
            }
        }
    }

    private void countCondBytes() {
        countCondBytes = new TreeMap<>();
        if(!countBytes.containsKey((byte)0)) {
            countBytes.put((byte)0, 1.0);
        }
        for(Byte b : countBytes.keySet()) {
            countCondBytes.put(b, new Predecessors(countBytes));
        }
        countCondBytes.get((byte)0).incEl(bytes[0]);
        for(int i = 0 ; i < allBytes-1 ; i++) {
            countCondBytes.get(bytes[i]).incEl(bytes[i+1]);
        }
    }

    public double condEnthropy() {
        double enthropy = 0;
        for(Map.Entry<Byte, Double> keyEntry : countBytes.entrySet()) {
            Byte key = keyEntry.getKey();
            double parent = keyEntry.getValue();
            Predecessors p = countCondBytes.get(key);
            for(Double val : p.getMap().values()) {
                double child = val;
                if(keyEntry.getValue() != 0 && val != 0)
                    enthropy += child  * (log2(parent) - log2(child));
            }
        }
        return enthropy/allBytes;
    }

    private double log2(double x)
    {
        return Math.log(x) / Math.log(2.0);
    }
}
