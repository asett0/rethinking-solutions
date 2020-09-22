# Chapter 1 Exercises

## Which of the expressions below correspond to the statement **the probability of rain on Monday?*

- Pr(rain)
- Pr(rain|Monday)
- Pr(Monday|rain)
- Pr(rain, Monday)/Pr(Monday)

(2), (4)

## 2E2

(3)

## 2E3

(1), (4)


## 2E4

Tossing the globe is not actually random. It's just that the deterministic processes that determine whether it lands on water or land are very complicated. 

## 2M1 

See code in `chap1.py`

## 2M2

See code in `chap2.py`

## 2M3

```
P(Earth | land) = P(land | Earth)P(Earth)/P(land)
P(land) = P(land | Earth) P(Earth) + P(land | Mars) P(Mars)
P(land) = 0.3 * 0.5  + 1*0.5
P(land) = 0.65
P(Earth | land) = 0.3 * 0.5 / 0.65
P(Eart | land) = 0.23076923076
```

## 2M4
Let B represent the number of black sides on the drawn card.

```
P(B=2| Black) = 2/3
P(B=1| Black) = 1/3
P(B=0| Black) = 0
```

## 2M5
Let A repesent the identifier of the card
```
P(A=0 | Black) = 2/5
P(A=1 | Black) = 2/5
P(A=2 | Black) = 1/5
P(A=3 | Black) = 0
```
P(A=0 | Black) = P(A=0, B=2 | Black) + P(A=1,  B=2 | Black ) = 4/5

## 2M6
```
P(First Card (B=2), Second Card (B=1) | black then white) = 2*1 / 8
P(First Card (B=2), Second Card (B=0)) = 2*2 / 8
P(First Card (B=1) | Second Card (B=0)) = 1 * 2 / 8
P(Anything else is 0)
P(First(Card(B=2))) = 0.75
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