# Задание 1
1.
$$
L = \{\omega \in \{a, b, c\}^*\mid |\omega|_c = 1 \}
$$
![FSA1](./images/f1.png)
2.
$$
L = \{\omega \in \{a, b\}^* \mid |\omega|_a \leq 2,|\omega|_b \geq 2 \}
$$
вершины имеют названия ij, где i - количество встретившихся "a", j - количество встретившихся "b"
![FSA2](./images/f2.png)

3. 
$$
L = \{\omega \in \{a, b\}^* \mid |\omega|_a \neq |\omega|_b\}
$$
т.к. $\overline L = \{\omega \in \{a, b\}^* \mid |\omega|_a = |\omega|_b\}$ не является регулярным, то и $L$ не является регулярным языком, значит не возможно построить автомат,  распознающий данный язык.
Доказательство:
$$
\begin{array}{rcl}
\omega &=& a^nb^n \in \overline L\\
|\omega| &=& 2n \geq n\\
xy &=&a^ia^j, \quad i + j \leq n\\
\omega &=& a^ia^ja^{n - i - j}b^n\\
\omega &=& a^ia^{jk}a^{n - i - j}b^n \notin \overline L \quad ,k > 1
\end{array}
$$
4.
$$
L = \{\omega \in \{a, b\}^* \mid \omega\omega = \omega\omega\omega \}
$$
Если $|\omega| > 0$, то $\omega\omega \neq \omega\omega\omega$ значит язык состоит из пустого слова, $\lambda\lambda = \lambda\lambda\lambda = \lambda$
![FSA3](./images/f3.png)

# Задание 2
1. 

$$
L_1 = \{\omega \in \{a, b\}^* \mid |\omega|_a \geq 2 \and |\omega|_b \geq 2 \} \\
L_1 = \{\omega \in \{a, b\}^* \mid |\omega|_a \geq 2\} \cap
  \{\omega \in \{a, b\}^* \mid |\omega|_b \geq 2\}
$$
  ![FSA4](./images/f4.png)
  ![FSA5](./images/f5.png)
$$
\begin{array}{rcl}
  \Sigma &=& {a, b} \\
  Q &=& \{AD, AE, AF, BD, BE, BF, CD, CE, CF \} \\
  S &=& AD \\
  T &=& CF
  \end{array}
$$
$$
\begin{array}{lll}
  \delta(AD, a) = BD & \delta(BD, a) = CD & \delta(CD, a) = CD& \\
  \delta(AD, b) = AE & \delta(BD, b) = BE & \delta(CD, b) = CE& \\
  \delta(AE, a) = BE & \delta(BE, a) = CE & \delta(CE, a) = CE& \\
  \delta(AE, b) = AF & \delta(BE, b) = BF & \delta(CE, b) = CF& \\
  \delta(AF, a) = BF & \delta(BF, a) = CF & \delta(CF, a) = CF& \\
  \delta(AF, b) = AF & \delta(BF, b) = BF & \delta(CF, b) = CF& \\
  \end{array}
$$
  ![FSA6](./images/f6.png)

2. 

$$
L_2 = \{\omega \in \{a, b\}^* \mid |\omega| \geq 3 \and |\omega| нечетно \} \\
L_2 = \{\omega \in \{a, b\}^* \mid |\omega| \geq 3\} \cap
\{\omega \in \{a, b\}^* \mid |\omega| нечетно\}
$$
![FSA7](./images/f7.png)
![FSA8](./images/f8.png)
$$
\begin{array}{rcl}
  \Sigma &=& {a, b} \\
  Q &=& \{AE, AF, BE, BF, CE, CF, DE, DF \} \\
  S &=& AE \\
  T &=& DF
\end{array}
$$
$$
\begin{array}{lll}
  \delta(AE, a) = BF & \delta(CE, a) = DF  \\
  \delta(AE, b) = BF & \delta(CE, b) = DF \\
  \delta(AF, a) = BE & \delta(CF, a) = DE \\
  \delta(AF, b) = BE & \delta(CF, b) = DE \\

  \delta(BE, a) = CF & \delta(DE, a) = DF \\
  \delta(BE, b) = CF & \delta(DE, b) = DF \\
  \delta(BF, a) = CE & \delta(DF, a) = DE \\
  \delta(BF, b) = CE & \delta(DF, b) = DE \\
\end{array}
$$

![FSA9](./images/f9.png)

Верхняя ветвь может быть удалена, т.к. ее вершины недостежимы

3. 

$$
L_1 = \{\omega \in \{a, b\}^* \mid |\omega|_a четно \and |\omega|_b \spaceкратно\spaceтрем \} \\
  L_1 = \{\omega \in \{a, b\}^* \mid |\omega|_a четно\} \cap
  \{\omega \in \{a, b\}^* \mid |\omega|_b \spaceкратно\spaceтрем\}
$$
![FSA10](./images/f10.png)
![FSA11](./images/f11.png)
$$
\begin{array}{rcl}
  \Sigma &=& {a, b} \\
  Q &=& \{AC, AD, AE, BC, BD, BE \} \\
  S &=& AC \\
  T &=& AC
\end{array}
$$
$$
\begin{array}{lll}
  \delta(AC, a) = BC & \delta(BC, a) = AC \\
  \delta(AC, b) = AD & \delta(BC, b) = BD \\
  \delta(AD, a) = BD & \delta(BD, a) = AD \\
  \delta(AD, b) = AE & \delta(BD, b) = BE \\
  \delta(AE, a) = BE & \delta(BE, a) = AE \\
  \delta(AE, b) = AC & \delta(BE, b) = BC \\
  \end{array}
$$
![FSA12](./images/f12.png)
4. $L_4 = \overline L_3$
![FSA13](./images/f13.png)
5. $L_5 = L_2 \setminus L_3 = L_2 \cap L_4$
![FSA14](./images/f14.png)
![FSA15](./images/f15.png)
$$
\begin{array}{rcl}
\Sigma &=& {a, b} \\
Q &=&\{AF, AG, AH, AI, AJ, AK, \\
     &&BF, BG, BH, BI, BJ, BK, \\
     &&CF, CG, CH, CI, CJ, BK, \\  
     &&DF, DG, DH, DI, DJ, DK, \\
     &&EF, EG, EH, EI, EJ, EK,\} \\
S &=& AF \\
T &=& \{DG, DH, DI, DJ, DK\}
\end{array}
$$
$$
\begin{array}{llll}
\delta(AF,a) = BG &
\delta(AF,b) = BK & 
\delta(AG,a) = BF & 
\delta(AG,b) = BH \\
\delta(AH,a) = BK & 
\delta(AH,b) = BI & 
\delta(AI,a) = BJ & 
\delta(AI,b) = BG \\
\delta(AJ,a) = BI & 
\delta(AJ,b) = BF & 
\delta(AK,a) = BH & 
\delta(AK,b) = BJ \\
\delta(BF,a) = CG &
\delta(BF,b) = CK &
\delta(BG,a) = CF &
\delta(BG,b) = CH \\
\delta(BH,a) = CK &
\delta(BH,b) = CI &
\delta(BI,a) = CJ &
\delta(BI,b) = CG \\
\delta(BJ,a) = CI &
\delta(BJ,b) = CF &
\delta(BK,a) = CH &
\delta(BK,b) = CJ \\
\delta(CF,a) = DG &
\delta(CF,b) = DK &
\delta(CG,a) = DF &
\delta(CG,b) = DH \\
\delta(CH,a) = DK &
\delta(CH,b) = DI &
\delta(CI,a) = DJ &
\delta(CI,b) = DG \\
\delta(CJ,a) = DI &
\delta(CJ,b) = DF &
\delta(CK,a) = DH &
\delta(CK,b) = DJ \\
\delta(DF,a) = EG &
\delta(DF,b) = EK &
\delta(DG,a) = EF &
\delta(DG,b) = EH \\
\delta(DH,a) = EK &
\delta(DH,b) = EI &
\delta(DI,a) = EJ &
\delta(DI,b) = EG \\
\delta(DJ,a) = EI &
\delta(DJ,b) = EF &
\delta(DK,a) = EH &
\delta(DK,b) = EJ \\
\delta(EF,a) = DG &
\delta(EF,b) = DK &
\delta(EG,a) = DF &
\delta(EG,b) = DH \\
\delta(EH,a) = DK &
\delta(EH,b) = DI &
\delta(EI,a) = DJ &
\delta(EI,b) = DG \\
\delta(EJ,a) = DI &
\delta(EJ,b) = DF &
\delta(EK,a) = DH &
\delta(EK,b) = DJ \\
\end{array}
$$
![FSA16](./images/f16.png)