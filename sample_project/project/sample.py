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
    parser = argparse.ArgumentParser(description='This is a sample project for'
                                                 ' trying out DevOps / MLOps'
                                                 ' in Python (currently adds'
                                                 ' two numbers)')

    parser.add_argument('smnd1', type=int, help='First summand')
    parser.add_argument('smnd2', type=int, help='Second summand')
    result = parser.parse_args()
    logger.info('Inputs: %d, %d', result.smnd1, result.smnd2)
    result_sum = Sample.add(result.smnd1, result.smnd2)
    logger.info('Result: %d', result_sum)


if __name__ == "__main__":
    LOGGING_FORMAT = '%(asctime)-15s: [%(name)s] %(message)s'
    # LOGGING_FORMAT = '[%(name)s] %(message)s'
    logging.basicConfig(level=logging.INFO,
                        format=LOGGING_FORMAT)
    logging.info('[ project.sample ]')
    logging.info('%s:: %s\n', platform.node(), ' '.join(sys.argv))
    main()
