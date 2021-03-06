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
        { 'actions': [
            value for value in
            get_actions(
                dat['coinsValue'],
                dat['originalWallet'],
                dat['finalWallet']
            )]},
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

    for value in iterate(sorted_values,
            Decimal("%.15g" % original),
            Decimal("%.15g" % final),
            content):
        yield {
                'action': 'add' if value > 0 else 'remove',
                'value': abs(value)
            }


def iterate(values, original, final, content=None):
    diff = final - original
    nearest_number = None

    if diff > 0:
        nearest_number = next(x for x in values if x <= diff)
    else:
        nearest_number = -min(content, key=lambda x:abs(x+diff))
        content.remove(abs(nearest_number))
    yield nearest_number

    original += nearest_number
    if original != final:
        for action in iterate(values, original, final, content):
            yield action



if __name__ == '__main__':
    run()
