#! /usr/bin/env python

import unittest

import click
from click.testing import CliRunner
from main import get_actions
from decimal import Decimal

class TestAll(unittest.TestCase):
    coinsValue = [
        100,
        10,
        0.5,
        1,
        5,
        0.1
    ]

    def execute_instructions(self,
            original,
            instructions):
        for action in instructions['actions']:
            original += action['value'] if action['action'] == 'add' else -action['value']
        return original

    def generic(self, tests):
        for tst in tests:
            actions = get_actions(
                    tst['coinsValue'],
                    tst['originalWallet'],
                    tst['finalWallet'])
            result = self.execute_instructions(
                    tst['originalWallet'],
                    actions)

            self.assertEqual(tst['finalWallet'], result)

    def test_single(self):
        tests = [
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 10)
            },
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 0.5)
            },
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 5)
            },
        ]
        self.generic(tests)


    def test_sum_from_zero(self):
        tests = [
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 27.5)
            },
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 99)
            },
            {
                'coinsValue': self.coinsValue,
                'originalWallet': 0,
                'finalWallet': Decimal("%.15g" % 32.8)
            },
        ]
        self.generic(tests)


if __name__ == '__main__':
    unittest.main()