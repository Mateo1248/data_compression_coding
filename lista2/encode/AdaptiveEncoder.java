package encode;

import utils.ASCIISignFrequency;
import utils.FileProcessing;
import utils.Utility;

import java.io.*;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

public class AdaptiveEncoder implements FileProcessing {

    private final String inputFile;
    private final String outFile;

    public AdaptiveEncoder(String inputFilePath, String outputFilePath) {
        this.inputFile = Objects.requireNonNull(inputFilePath);
        if (outputFilePath == null || outputFilePath.length() == 0)
            outputFilePath = System.getProperty("user.dir").concat("/encodedFile.bin");

        this.outFile = outputFilePath;
    }

    private void compress(InputStream in, BitOutputStream out) throws IOException {
        int[] initFreqs = new int[257];
        Arrays.fill(initFreqs, 1);
        ASCIISignFrequency freqs = new ASCIISignFrequency(initFreqs);
        ArithmeticEncoder enc = new ArithmeticEncoder(30, out);
        while (true) {
            int symbol = in.read();
            if (symbol == -1)
                break;
            enc.write(freqs, symbol);
            freqs.increment(symbol);
        }
        enc.write(freqs, 256);
        enc.finish();
        this.printCompressInfo(freqs,initFreqs.length);
    }

    @Override
    public void startProcessingFile() throws IOException {
        try (InputStream in = new BufferedInputStream(new FileInputStream(inputFile));
             BitOutputStream out = new BitOutputStream(new BufferedOutputStream(new FileOutputStream(outFile)))) {
            this.compress(in, out);
        }
    }

    public void printCompressInfo(ASCIISignFrequency freqs, int initFreq) throws FileNotFoundException {
        for (int i = 0; i < freqs.getFrequencies().length; i++)
            freqs.getFrequencies()[i]--;

        final int[] ints = Arrays.copyOf(freqs.getFrequencies(), 256);
        System.out.println(String.format("Entropy: %1.5f", Utility.countEntropy(freqs.getTotal() -initFreq, ints)));
        final List<Long> filesSize = Utility.getFilesSize(inputFile, outFile);
	System.out.println(String.format("Average length: %1.5f", ((double)filesSize.get(1)/freqs.getTotal())*8));
        System.out.println(String.format("Compression rate: %1.5f", (double)filesSize.get(0)/filesSize.get(1)));

    }

}
