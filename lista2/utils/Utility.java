package utils;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Arrays;
import java.util.List;

import static java.util.stream.Collectors.toList;


public final class Utility {

    public static List<Long> getFilesSize(String ...filesPaths) throws FileNotFoundException {
        return Arrays.stream(filesPaths)
                .map(path -> new File(path).length())
                .collect(toList());
    }

    public static double countEntropy(long allSymbolsOccurrences, int[] symbolsData) {
        double entropy = 0.0D;
        double logFromAll = log2(allSymbolsOccurrences);
        for (int data : symbolsData) {
            if (data <= 0) continue;
            entropy += data * (logFromAll - log2(data));
        }
        return entropy/allSymbolsOccurrences;
    }

    public static double log2(double x) {
        return Math.log(x)/Math.log(2);
    }

}
