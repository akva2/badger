from pathlib import Path

import numpy as np
import pandas as pd

from badger import Case


DATADIR = Path(__file__).parent / 'data'


def read_file(path: Path) -> str:
    with open(path, 'r') as f:
        return f.read()


def check_df(left, right):
    to_remove = [c for c in left.columns if c.startswith('walltime/')]
    pd.testing.assert_frame_equal(
        left.drop(columns=to_remove).sort_index(axis=1),
        right.sort_index(axis=1)
    )


def test_echo():
    case = Case(DATADIR / 'run' / 'echo')
    case.clear_cache()
    case.run()

    with case.dataframe(modify=False) as data:
        check_df(data, pd.DataFrame(
            index=pd.MultiIndex.from_product(
                [[1, 2, 3], ['a', 'b', 'c']],
                names=['alpha', 'bravo'],
            ),
            data={
                '_done': [True] * 9,
                '_index': pd.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=pd.Int64Dtype()),
                'alpha': pd.array([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype=pd.Int64Dtype()),
                'bravo': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
                'charlie': pd.array([1, 1, 1, 3, 3, 3, 5, 5, 5], dtype=pd.Int64Dtype()),
                'a': pd.array([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype=pd.Int64Dtype()),
                'b': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
                'c': [1., 1., 1., 3., 3., 3., 5., 5., 5.],
            }
        ))


def test_cat():
    case = Case(DATADIR / 'run' / 'cat')
    case.clear_cache()
    case.run()

    with case.dataframe(modify=False) as data:
        check_df(data, pd.DataFrame(
            index=pd.MultiIndex.from_product(
                [[1, 2, 3], ['a', 'b', 'c']],
                names=['alpha', 'bravo'],
            ),
            data={
                '_done': [True] * 9,
                '_index': pd.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=pd.Int64Dtype()),
                'alpha': pd.array([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype=pd.Int64Dtype()),
                'bravo': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
                'charlie': pd.array([1, 1, 1, 3, 3, 3, 5, 5, 5], dtype=pd.Int64Dtype()),
                'a': pd.array([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype=pd.Int64Dtype()),
                'b': ['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'],
                'c': [1., 1., 1., 3., 3., 3., 5., 5., 5.],
                'a_auto': pd.array([1, 1, 1, 2, 2, 2, 3, 3, 3], dtype=pd.Int64Dtype()),
            }
        ))


def test_files():
    case = Case(DATADIR / 'run' / 'files')
    case.clear_cache()
    case.run()

    for a in range(1,4):
        for b in 'abc':
            path = DATADIR / 'run' / 'files' / '.badgerdata' / f'{a}-{b}'
            assert read_file(path / 'template.txt') == f'a={a} b={b} c={2*a-1}\n'
            assert read_file(path / 'other-template.txt') == f'a={a} b={b} c={2*a-1}\n'
            assert read_file(path / 'non-template.txt') == 'a=${alpha} b=${bravo} c=${charlie}\n'
            assert read_file(path / 'some' / 'deep' / 'directory' / 'empty1.dat') == ''
            assert read_file(path / 'some' / 'deep' / 'directory' / 'empty2.dat') == ''
            assert read_file(path / 'some' / 'deep' / 'directory' / 'empty3.dat') == ''


def test_capture():
    case = Case(DATADIR / 'run' / 'capture')
    case.clear_cache()
    case.run()

    with case.dataframe(modify=False) as data:
        check_df(data, pd.DataFrame(
            index=pd.MultiIndex.from_product(
                [[1.234, 2.345, 3.456], [1, 2, 3]],
                names=['alpha', 'bravo'],
            ),
            data={
                '_done': [True] * 9,
                '_index': pd.array([0, 1, 2, 3, 4, 5, 6, 7, 8], dtype=pd.Int64Dtype()),
                'alpha': [1.234, 1.234, 1.234, 2.345, 2.345, 2.345, 3.456, 3.456, 3.456],
                'bravo': pd.array([1, 2, 3, 1, 2, 3, 1, 2, 3], dtype=pd.Int64Dtype()),
                'firstalpha': [1.234, 1.234, 1.234, 2.345, 2.345, 2.345, 3.456, 3.456, 3.456],
                'lastalpha': [4.936, 4.936, 4.936, 9.38, 9.38, 9.38, 13.824, 13.824, 13.824],
                'allalpha': [
                    [1.234, 2.468, 3.702, 4.936], [1.234, 2.468, 3.702, 4.936], [1.234, 2.468, 3.702, 4.936],
                    [2.345, 4.690, 7.035, 9.380], [2.345, 4.690, 7.035, 9.380], [2.345, 4.690, 7.035, 9.380],
                    [3.456, 6.912, 10.368, 13.824], [3.456, 6.912, 10.368, 13.824], [3.456, 6.912, 10.368, 13.824]
                ],
                'firstbravo': pd.array([1, 2, 3, 1, 2, 3, 1, 2, 3], dtype=pd.Int64Dtype()),
                'lastbravo': pd.array([4, 8, 12, 4, 8, 12, 4, 8, 12], dtype=pd.Int64Dtype()),
                'allbravo': [
                    [1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12],
                    [1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12],
                    [1, 2, 3, 4], [2, 4, 6, 8], [3, 6, 9, 12],
                ],
            }
        ))


def test_failing():
    case = Case(DATADIR / 'run' / 'failing')
    case.clear_cache()
    case.run()

    with case.dataframe(modify=False) as data:
        check_df(data, pd.DataFrame(
            index=pd.Int64Index([0, 1], name='retcode'),
            data={
                '_done': [True, True],
                '_index': pd.array([0, 1], dtype=pd.Int64Dtype()),
                'retcode': pd.array([0, 1], dtype=pd.Int64Dtype()),
                'before': pd.array([12, 12], dtype=pd.Int64Dtype()),
                'return': pd.array([0, 1], dtype=pd.Int64Dtype()),
                'next': pd.array([0, pd.NA], dtype=pd.Int64Dtype()),
                'after': pd.array([13, pd.NA], dtype=pd.Int64Dtype()),
            }
        ))


def test_stdout():
    case = Case(DATADIR / 'run' / 'stdout')
    case.clear_cache()
    case.run()

    path = DATADIR / 'run' / 'stdout' / '.badgerdata'
    assert read_file(path / 'out-0' / 'good.stdout') == 'stdout 0\n'
    assert read_file(path / 'out-0' / 'good.stderr') == 'stderr 0\n'
    assert read_file(path / 'out-0' / 'bad.stdout') == 'stdout 0\n'
    assert read_file(path / 'out-0' / 'bad.stderr') == 'stderr 0\n'
    assert read_file(path / 'out-1' / 'good.stdout') == 'stdout 1\n'
    assert read_file(path / 'out-1' / 'good.stderr') == 'stderr 1\n'
    assert read_file(path / 'out-1' / 'bad.stdout') == 'stdout 1\n'
    assert read_file(path / 'out-1' / 'bad.stderr') == 'stderr 1\n'
