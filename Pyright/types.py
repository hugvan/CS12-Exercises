from typing import TypeVar, Sequence, Iterable, Mapping, MutableSequence

T = TypeVar("T")
U = TypeVar("U")

def f1(seq: Sequence[T]) -> Sequence[T]:
    return seq[::-1]

def f2(xss: Iterable[Iterable[T]]) -> Iterable[T]:
    return [x for xs in xss for x in xs]

def f(m: Mapping[T, U]) -> Mapping[U, Sequence[T]]:
    ret: dict[U, list[T]] = {}
 
    for k, v in m.items():
        ret.setdefault(v, []).append(k)
 
    return ret



def tup_to_list() -> list[int]:
    return (1, 2, 3)

def list_to_tup() -> tuple[int, ...]:
    return [1, 2, 3]

def list_to_seq() -> Sequence[int]:
    return [1, 2, 3]

def tup_to_seq() -> Sequence[int]:
    return (1, 2, 3)

def list_to_mseq() -> MutableSequence[int]:
    return [1, 2, 3]

def tup_to_mseq() -> MutableSequence[int]:
    return (1, 2, 3)



def A(x: list[int]):
    ...

A(list())
A(tuple())
A(list_to_seq())
A(list_to_mseq())
A(dict())

def B(x: tuple[int, ...]):
    ...

B(list())
B(tuple())
B(list_to_seq())
B(list_to_mseq())
B(dict())

def C(x: Sequence[int]):
    ...

C(list())
C(tuple())
C(list_to_seq())
C(list_to_mseq())
C(dict())

def D(x: MutableSequence[int]):
    ...

D(list())
D(tuple())
D(list_to_seq())
D(list_to_mseq())
D(dict())