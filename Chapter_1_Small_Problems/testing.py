import unittest
from exercises import ex_fibonacci, CompressedGene, BitArray, towers_of_hanoi, Stack


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, 1)  # add assertion here

    def testFibonacci(self):
        self.assertEqual(ex_fibonacci(5), 5)
        self.assertEqual(ex_fibonacci(0), 0)
        self.assertEqual(ex_fibonacci(7), 13)
        self.assertEqual(ex_fibonacci(12), 144)
        self.assertEqual(ex_fibonacci(4), 3)

    def testCompression(self):
        gene: str = "ACTG"
        compressed_gene: CompressedGene = CompressedGene(gene)
        bit_sequence: BitArray = BitArray(286)
        self.assertEqual(gene, compressed_gene.decompress())
        self.assertEqual(str(compressed_gene.bit_array), str(bit_sequence))

    def testTowers(self):
        source = Stack[int]()
        target = Stack[int]()
        source_before = Stack[int]()
        auxiliary = [Stack[int]() for _ in range(2)]  # You can increase or decrease the number of auxiliary towers
        # Push disks onto the source tower (larger number on bottom)
        for i in range(5, 0, -1):
            source.push(i)
            source_before.push(i)
        towers_of_hanoi(5, source, target, auxiliary)
        for _ in range(5):
            self.assertEqual(target.pop(), source_before.pop())
        self.assertEqual(source.isempty(), True)



if __name__ == '__main__':
    unittest.main()
