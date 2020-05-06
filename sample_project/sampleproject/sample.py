import sys
import platform
import logging
import argparse


class Sample():

    @staticmethod
    def add(a, b):
        print(a, b)
        return a+b+1


def main():
    logger = logging.getLogger('sample::main')
    logger.info('%s:: %s\n', platform.node(), ' '.join(sys.argv))
    descr = ''.join(('This is a sample project for trying out DevOps in ',
                     'Python. The app adds two numbers and the result is off ',
                     'by one. (Intended for experimenting with a failing ',
                     'unit test.)'))
    parser = argparse.ArgumentParser(description=descr)

    parser.add_argument('smnd1', type=int, help='First summand')
    parser.add_argument('smnd2', type=int, help='Second summand')
    result = parser.parse_args()
    logger.info('Inputs: %d, %d', result.smnd1, result.smnd2)
    result_sum = Sample.add(result.smnd1, result.smnd2)
    logger.info('Result: %d', result_sum)


if __name__ == "__main__":
    main()
