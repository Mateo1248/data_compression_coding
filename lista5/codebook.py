import numpy as np
import random
import time
from dataclasses import dataclass


from pixel_map import Pixel
from tga import get_closest_vector


@dataclass
class Partition:
    total_vector: np.ndarray
    total_distance: int = 0
    count: int = 0


class CodebookFactory:
    """
        Creates codebook for vector quantization using LBG algorithm.
    """

    def __init__(self, pixel_table, perturbation_vector, block_side, epsilon):
        self.pixel_map = pixel_table
        self.perturbation_vector = perturbation_vector
        self.block_side = block_side
        self.vector_size = block_side**2
        self.blocks = pixel_table.get_blocks(self.block_side)
        self.epsilon = epsilon


    def get_first_point(self):
        return self.get_average_color(self.blocks)


    def get_average_color(self, blocks):
        total = np.array([(0,0,0) for _ in range(self.vector_size)])
        count = 0
                
        for vector in blocks:
            total += vector
            count += 1
        if count == 0:
            return random.choice(self.blocks)
        return total//count


    def get_partition_mean(self, partition):
        if partition.count == 0:
            return random.choice(self.blocks)
        return partition.total_vector//partition.count


    def calculate_new_codebook(self, codebook, partitions):
        for i in range(len(partitions)):
            codebook[i] = self.get_partition_mean(partitions[i])


    def create_codebook(self, iterations):
        codebook = np.empty(2**iterations, dtype=object)
        codebook[0] = self.get_first_point()

        for it in range(iterations):
            length = 2**it
            for i in range(length):
                codebook[length + i] = (codebook[i]+self.perturbation_vector) % 256
            codebook = self.lbg(codebook, length*2)
        return codebook


    def lbg(self, codebook, codebook_size):
        prev_distortion = float('inf')
        while True:
            partitions = self.generate_partitions(codebook, codebook_size)
            distortion = calculate_distortion(partitions)
            change = (prev_distortion - distortion)/distortion
            
            if change < self.epsilon:
                return codebook

            self.calculate_new_codebook(codebook, partitions)
            prev_distortion = distortion


    def generate_partitions(self, codebook, codebook_size):
        partitions = np.array(
            [
                Partition(
                    np.array([(0,0,0) for _ in range(self.vector_size)], dtype=int), 
                    0, 
                    0
                ) for _ in range(codebook_size)
            ], 
            dtype=Partition
        )

        for block in self.blocks:
            min_val, min_idx = get_closest_vector(block, codebook, codebook_size)
            partition = partitions[min_idx]
            partition.total_vector += block
            partition.total_distance += min_val
            partition.count += 1
        return partitions


def calculate_distortion(partitions):
    s = 0
    for partition in partitions:
        if partition.count > 0:
            s += partition.total_distance/partition.count
    return s/len(partitions)
