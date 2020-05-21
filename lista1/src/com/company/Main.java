package com.company;

public class Main {

    public static void main(String[] args) {

        if(args.length > 1) {
            Enthropy e = new Enthropy("./tests/" + args[1]);
            e.result();
        }
        else {
            String[] tests = {
                    "test1.bin",
                    "test2.bin",
                    "test3.bin",
                    "pan-tadeusz-czyli-ostatni-zajazd-na-litwie.txt"
            };
            for (String test : tests) {
                Enthropy e = new Enthropy("./tests/" + test);
                System.out.println("############################################\n" + test);
                e.result();
            }
        }
    }
}
