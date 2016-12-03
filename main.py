#! /usr/bin/env python

import click
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


@click.command()
@click.argument('f',
        type=click.File(),
        default='input.txt')
def run(f):
    dat = json.loads(f.read())
    click.echo(json.dumps(
        get_actions(
            dat['coinsValue'],
            dat['originalWallet'],
            dat['finalWallet']),
        cls=DecimalEncoder))


def get_actions(values, original, final):
    sorted_values = sorted([
        Decimal("%.15g" % v)
        for v in values
        ], reverse=True)
    content = None
    if original > 0:
        content = [
            x for x in
            iterate(sorted_values,
                Decimal("%.15g" % 0),
                Decimal("%.15g" % original))
        ]

    return { 'actions': [
        {
            'action': 'add' if value > 0 else 'remove',
            'value': abs(value)
        }
        for value in
        iterate(sorted_values,
            Decimal("%.15g" % original),
            Decimal("%.15g" % final),
            content)
    ]}


def iterate(values, original, final, content=None):
    diff = final - original
    biggest_number = None
    if diff > 0:
        biggest_number = next(x for x in values if x <= diff)
    else:
        biggest_number = next(-x for x in content if x <= abs(diff))
    original += biggest_number
    yield biggest_number
    if original != final:
        for action in iterate(values, original, final, content):
            yield action



if __name__ == '__main__':
    run()
