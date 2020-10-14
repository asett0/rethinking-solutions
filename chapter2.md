# Chapter 1 Exercises

(2), (4)

## 2E2

(3)

## 2E3

(1), (4)


## 2E4

Tossing the globe is not actually random. It's just that the deterministic processes that determines whether it lands on water or land are very complicated. 

## 2M1 

See code in `chap2.py`

## 2M2

See code in `chap2.py`

## 2M3

```
P(Earth | land) = P(land | Earth)P(Earth)/P(land)
P(land) = P(land | Earth) P(Earth) + P(land | Mars) P(Mars)
P(land) = 0.3 * 0.5  + 1 * 0.5
P(land) = 0.65
P(Earth | land) = 0.3 * 0.5 / 0.65
P(Earth | land) = 0.2307
```

## 2M4
Let B represent the number of black sides on the drawn card.
Let SS represent the the shown side of the drawn card 
```
P(B=2 | SS=Black) = 2/N
P(B=1 | SS=Black) = 1/N
P(B=0 | SS=Black) = 0/N
2/N + 1/N + 0/N = 1
N = 3

P(B=2 | SS=Black) = 2/3
P(B=1 | SS=Black) = 1/3
P(B=0 | SS=Black) = 0
```

## 2M5
```
P(B=2 | SS=Black) = 4/N
P(B=1 | SS=Black) = 1/N
P(B=0 | SS=Black) = 0/N
4/N + 1/N + 0/N = 1
N = 5

P(B=2 | SS=Black) = 4/5
P(B=1 | SS=Black) = 1/5
P(B=0 | SS=Black) = 0/5
```

## 2M6
```
P(B=2 | SS=Black) = 2*1/N
P(B=1 | SS=Black) = 1*2/N
P(B=0 | SS=Black) = 0*3/N
2/N + 2/N + 0/N = 1
N = 4

P(B=2 | SS=Black) = 1/2
P(B=1 | SS=Black) = 1/2
P(B=0 | SS=Black) = 0
```

## 2M7
Let SSFC represent the shown side of the first drawn card
Let SSSC represent the shown side of the second drawn card
Let FB represent the number of black sides on the first drawn card
Let SB represent the number of black sides on the second drawn card
```
P(FB=0, SB=1 | FB=Black, SB=White) = 0*1/N 
P(FB=0, SB=2 | FB=Black, SB=White) = 0*0/N
P(FB=1, SB=0 | FB=Black, SB=White) = 1*2/N
P(FB=1, SB=2 | FB=Black, SB=White) = 1*0/N
P(FB=2, SB=0 | FB=Black, SB=White) = 2*2/N
P(FB=2, SB=1 | FB=Black, SB=White) = 2*1/N

0/N + 0/N + 2/N + 0/N + 4/N + 2/N = 1
N=8

P(FB=2 | FB=Black, SB=White) = P(FB=2, SB=0 | FB=Black, SB=White) + P(FB=2, SB=1 | FB=Black, SB=White)
P(FB=2 | FB=Black, SB=White) = 4/8 + 2/8
P(FB=2 | FB=Black, SB=White) = 3/4
```

## 2H1
```
P(Twins| A) = 0.1
P(Twins | B) = 0.2 
P(Second Birth Twins | First Birth Twins) = P(First Birth Twins, Second Birth Twins)/ P(First Birth Twins)

P(First Birth Twins) = P(First Birth Twins | A) P(A) + P(First Birth Twins | B)  P (B)

P(First Birth Twins) = 0.15

P(First Birth Twins, Second Birth Twins) = P(First Birth Twins, Second Birth Twins|A)P(A) + P(First Birth Twins, Second Birth Twins | B) P(B) 
P(First Birth Twins, Second Birth Twins) = 0.1*0.1*0.5 + 0.2*0.2*0.5 = 0.025
P(Second Birth Twins | First Birth Twins) = 0.025 / 0.15 = 0.1666

```


## 2H2

```P(A | First Birth Twins) = P(First Birth Twins | A)* P(A)/P(First Birth Twins)
P(A | First Birth Twins) = 0.1 * 0.5 / 0.15
P(A | First Birth Twins) = 0.33333
```

## 2H3
```
P(A | Second Birth Single, First Birth Twins) = P(Second Birth Single , First Birth Twins | A) P(A)/P(Second Birth Single , First Birth Twins)
P(A | Second Birth Single, First Birth Twins) = 0.09 * 0.5 / 0.125
P(A | Second Birth Single, First Birth Twins) = 0.36
```
Alternatively
```
P(A | Second Birth Single, First Birth Twins)  = P(Second Birth Single | A, First Birth Twin) P(A| First Birth Twin)
/P(Second Birth Single | First Birth Twins) = 0.36
```

## 2H4
```
P(Test is A | A) = 0.8
P(Test is B | B) = 0.65

P(A | Test is A) = P(Test is A | A)*P(A)/P(Test is A)
P(A | Test is A) = 0.8 * 0.5 / (0.8*0.5 + 0.35 * 0.5)
P(A | Test is A) = 0.69565
```
```
P(A | Test is A, Second Birth Single, First Birth Twins) = P(Test is A | A, First Birth is Twins, Second Birth is Single) P(A | First Birth Twins, Second Birth Single)/ P(Test is A | First Birth Twins, Second Birth Single)
P(A | Test is A, Second Birth Single, First Birth Twins) = 0.8 * 0.36 / (0.8 * 0.36 + 0.35 * 0.64 )
P(A | Test is A, Second Birth Single, First Birth Twins) = 0.5625
```