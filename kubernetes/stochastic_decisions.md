# Implementation of Stochastic Decision

## Introduction

## Definition of Stochastic Decision
Here I will define this decision mathematically: $Q$ is a decision, yielding {0, 1}. $Q$ is a stochastic function of minimum number of data required $m$, DP loss allowed $\epsilon$, $\delta$, and total number of the data qualified for the application $N$. 

$$ Q_{m, \epsilon, \delta}(N) \in \{0, 1\} $$

$Q(N)$ will be used in the following for simplicity, because $m$, $\epsilon$, and $\delta$ are fixed input. Consider two neighbor dataset $x$ and $y$, and their number of data is $N$ and $N+1$, ($\epsilon, \delta$)-DP is defined to be

$$Pr(Q(N+1) = 1) \leq e^{\epsilon} Pr(Q(N) = 1) + \delta$$

$$Pr(Q(N) = 0) \leq e^{\epsilon} Pr(Q(N+1) = 0) + \delta$$

Since $Q(N)$ is a monotonic increasing given $N$, thus I don't have to consider the cases switching LHS and RHS of the above inequalities. Therefore, any stochastic query meeting these two inequalities is a qualified stochastic decision. In addition, to make the decision practically, one more constrain can be added:

$$Pr(Q(m) = 1) \geq \frac{1}{2},$$

which reflects the meaning of $m$. 


## Theorems

**Theorem 1.** $x$ is a scalar variable, and $f(x)$ is a monotonically decreasing function. If 

\begin{align}
    f(a) - f(a + 1) \leq f(b) - f(b + 1), \tag{5}
\end{align}


and $a < b$, and that 


\begin{align}
   f(b) \leq \epsilon f(b+1) + \delta, \tag{6}
\end{align}

where $\epsilon \geq 1$ and $\delta \geq 0$, then


\begin{align}
   f(a) \leq \epsilon f(a+1) + \delta \tag{7}
\end{align}

is also guaranteed.


*Proof of Theorem 1.* 

Modify the Ineq. (6) as

\begin{align}
    f(b) - f(b+1) \leq (\epsilon - 1) f(b+1) + \delta. \tag{8}
\end{align}

Since $\epsilon - 1 \geq 0$ and $f(b+1) \leq f(a+1)$,

\begin{align}
    (\epsilon - 1) f(b+1) + \delta \leq (\epsilon - 1) f(a+1) + \delta. \tag{9}
\end{align}

Combine Ineq.(5), (8) and (9),

\begin{align}
    f(a) - f(a+1) \leq (\epsilon - 1) f(a+1) + \delta \tag{10} \\
    \Rightarrow f(a) \leq \epsilon f(a+1) + \delta. \tag{11}
\end{align}

**Lemma 1.** If $x$ is a scalar variable and $f(x)$ is a monotonically decreasing and derivable function, and that 

\begin{align}
    f'(a) \geq f'(b), \tag{12}
\end{align}

where $a + 1\leq b$, then Ineq. (7) can be derived from Ineq. (6).


*Proof of Lemma 1.* 

Given the Lagrange's Mean Value Theorem, 

\begin{align}
    f(a) - f(b) = f'(\xi)(a-b), \tag{13}
\end{align}

where $a < \xi < b$, and substitute with (a, a+1) and (b, b+1), respectively, then it becomes

\begin{align}
    f(a) - f(a+1) = -f'(\xi_{a}), \tag{14} \\
    f(b) - f(b+1) = -f'(\xi_{b}). \tag{15}
\end{align}

Given $a < \xi_{a} < a + 1 \leq b < \xi_{b} < b + 1$, Ineq. (12) becomes

\begin{align}
    -f'(\xi_{a}) \leq -f'(\xi_{b}) \tag{16}.
\end{align}

Combining Ineq. (14), (15), and (16) yields (5). Given Theorem 1., the lemma is proved.

## 4. Laplace Noise Decision

The decision should count the total number of data, add a Laplace noise to the counting to achieve DP, and compare the result with a value. If the result is larger  than or equals the value, the decision return `True`, else `False`.

\begin{align}
    Q(N) = N + L(\frac{1}{\epsilon}) \geq k, \tag{4.1}\\
\end{align}

where $N$ is the total counting, $L$ is the Laplace noise, and $k$ is a constant, which is a function of the minimum number of data $m$ in practice. Since Laplace mechanism has already provided ($\epsilon, \delta$)-DP, there is no need to justify this implementation.

Now, I am going to calculate the $Pr(Q(N)=1)$. The PDF of $L(\frac{1}{\epsilon})$ is

\begin{align}
    L(x|\frac{1}{\epsilon}) = \frac{\epsilon}{2} e^{-\epsilon |x|}, \tag{4.1}
\end{align}

if $N < k$,

\begin{align}
    Pr(N + L(\frac{1}{\epsilon}) \geq k) = \int_{k-N}^{\infty} \frac{\epsilon}{2} e^{-\epsilon x}, \\
    = -\frac{\epsilon}{2} e^{-\epsilon x} |_{k-N}^{\infty}=\frac{1}{2}e^{\epsilon (N-k)}, \tag{4.2}
\end{align}

Similarly, if $N \geq k$,

\begin{align}
    Pr(N + L(\frac{1}{\epsilon}) \geq k) =\frac{1}{2} + \int_{k-N}^{0} \frac{\epsilon}{2} e^{\epsilon x}, \\
    = 1 - \frac{1}{2} e^{\epsilon (k-N)}. \tag{4.3}
\end{align}


If $k=m$, then $Pr(Q(m) = 1) = \frac{1}{2}$. If we want $Pr(Q(m) = 1) = p > \frac{1}{2}$, then $k$ should be smaller than $m$. Based on Eq. (4.3), 

\begin{align}
    1 - \frac{1}{2} e^{\epsilon (k-m)} = p, \tag{4.4}\\
    k = m + \frac{\ln[2(1-p)]}{\epsilon}. \tag{4.5}
\end{align}

If $p=0.99$ and $\epsilon = 10^{-3}$, then $k = m - 3912$.

If we prefer a conservative strategy, i.e. $Pr(Q(m) = 1) = p < \frac{1}{2}$, similarly we have

\begin{align}
    \frac{1}{2} e^{\epsilon (m-k)} = p, \tag{4.6}\\
    k = m - \frac{\ln(2p)}{\epsilon}. \tag{4.7}
\end{align}

If $p=0.01$ and $\epsilon = 10^{-3}$, then $k = m + 3912$. It can be found that there is an interval of around 8000 between the positions of $p=0.01$ and $p=0.99$ when $\epsilon = 10^{-3}$. That is to say, if I set the minimum requirement of 100,000 data, $\epsilon = 10^{-3}$, and choose a conservative strategy, the dataset needs to have more than 108,000 data to ensure the decision can give `True` with the probability higher than 99%.

## 5. Cutoff Exponential Implementation

This implementation has the basic idea: if total counting $N$ equals or larger than $m$, then the decision should always yield `True`. That is

\begin{align}
    Pr(Q(N \geq m) = 1) = 1. \tag{5.1} 
\end{align}


Also when $N < m$, the implementation needs to provide a $\epsilon$-DP guarantee, so the probability of yielding `True` should maintain a relationship like

\begin{align}
    Pr(Q(N) = 1) = e^{\epsilon} Pr(Q(N - 1) = 1). \tag{5.2} 
\end{align}


Combine (5.1) and (5.2), we can get for every $N \leq m$,

\begin{align}
    Pr(Q(N) = 1) = e^{\epsilon (N - m)}, \tag{5.3}\\
    Pr(Q(N) = 0) = 1 - e^{\epsilon (N - m)}. \tag{5.4}
\end{align}

When $N = m$, 

\begin{align}
    Pr(Q(m-1) = 0) \leq e^{\epsilon} Pr(Q(m) = 0) + \delta, \tag{5.5}\\ 
    \Rightarrow 1 - e^{-\epsilon} \leq e^{\epsilon} * 0 + \delta. \tag{5.6}
\end{align}

Thus the minimum of $\delta$ is $1 - e^{-\epsilon}$. Given the minimum $\delta$ and (5.2), 

\begin{align}
    Pr(Q(N+1) = 1) \leq e^{\epsilon} Pr(Q(N) = 1) + 1 - e^{-\epsilon}\tag{5.7}
\end{align}

is always correct by the definition. Switching LHS and RHS is also correct, because $Pr(Q(N) = 1)$ is always smaller than $Pr(Q(N + 1) = 1)$.

Now the question becomes proving the correctness of

\begin{align}
    Pr(Q(N) = 0) \leq e^{\epsilon} Pr(Q(N+1) = 0) + 1 - e^{-\epsilon} \tag{5.8}
\end{align}


for every $N < m$. Given $Pr(Q(N) = 0)$ is a monotonically decreasing and the proof of (5.5), if we can prove 

\begin{align}
    \frac{d}{dx}Pr(Q(x=a) = 0) \geq \frac{d}{dx}Pr(Q(x=b) = 0), \tag{5.9}
\end{align}

where $a + 1 \leq b$, then the Lemma 1. could lead to the proof of Ineq. (5.8).

For simplicity, define $f(x) = Pr(Q(x) = 0)$, then

\begin{align}
    f'(x) = \frac{d}{dx} (1 - e^{\epsilon (x - m)}), \tag{5.10}\\
    \Rightarrow f'(x) = - e^{-\epsilon m} \frac{d}{dx}  e^{\epsilon x} = - e^{-\epsilon m} \epsilon e^{\epsilon x}. \tag{5.11}
\end{align}

Since $f'(x)$ is apparently a monotonically decreasing function, Ineq. (5.9) is proved. Ineq (5.8) is proved accordingly. Therefore, this Cutoff Exponential Implementation provides ($\epsilon, 1 - e^{-\epsilon}$)-DP guarantee.

## 6. Generalized Laplace Noise Decision

Laplace noise is pure $\epsilon$-DP. What about users want to utilize some budget of $\delta$. This section will start from the definition of DP and derive a general model. Laplace Noise Decision is found to be a special case of this model. 

Here is the derivation of the model. $Q$ is the stochastic decision, and $f(n) = Pr(Q(m) = 1)$. If $f(n)$ is monotonically increasing, based on the definition of DP, we have:


\begin{align}
    f(n) \leq e^{\epsilon} f(n-1) + \delta, \tag{6.1}\\
    1 - f(n-1) \leq e^{\epsilon} (1 - f(n)) + \delta \tag{6.2}
\end{align}

Move $f(n-1)$ to one side,

\begin{align}
    (f(n) - \delta) e^{-\epsilon} \leq  f(n-1), \tag{6.3}\\
    1 - \delta - e^{\epsilon} (1 - f(n)) \leq f(n-1)  \tag{6.4}.
\end{align}

Therefore,

\begin{align}
    \min f(n-1) = \max [(f(n) - \delta) e^{-\epsilon}, 1 - \delta - e^{\epsilon} (1 - f(n))]. \tag{6.5}
\end{align}

Define 

\begin{align}
    g(p) = [(p - \delta) e^{-\epsilon}] - [1 - \delta - e^{\epsilon} (1 - p)] \\
    = (p - \delta) e^{-\epsilon} - 1 + \delta + e^{\epsilon} (1 - p), \tag{6.6}
\end{align}

where $p = f(n) \in [0, 1]$. Set $p=1$,

\begin{align}
    g(1) = (1 - \delta)e^{-\epsilon} - 1 + \delta = (1 - \delta)(e^{-\epsilon} - 1) \leq 0, \tag{6.7}
\end{align}

given $\epsilon \geq 0$ and $\delta \leq 1$. Also set $p=0$,

\begin{align}
    g(0) = - \delta e^{-\epsilon} - 1 + \delta + e^{\epsilon} = \delta (1 - e^{-\epsilon}) + e^{\epsilon} - 1 \geq 0, \tag{6.8}
\end{align}

given $1 - e^{-\epsilon} \leq 0$ and $e^{\epsilon} - 1 \geq 0$.

Also given 

\begin{align}
    g'(p) = e^{-\epsilon} - e^{\epsilon} \leq 0 \tag{6.9},
\end{align}

$g(p)$ should have one and only one root when $p \in [0, 1]$. The root $p_0$ can be computed to be

\begin{align}
    p_0 = \frac{e^{\epsilon} - 1 + \delta(1 - e^{-\epsilon})}{e^{\epsilon} - e^{-\epsilon}}. \tag{6.10}
\end{align}

That is to say, when $f(n) > p$, LHS of (6.4) is always larger than the LHS of (6.3), vice versa, i.e. the solution of f(n) maintaining DP is derived to be

\begin{align}
    f(n-1) = (f(n) - \delta) e^{-\epsilon}, \text{ when } f(n) \leq p_0 \tag{6.11}\\
    f(n-1) = 1 - \delta - e^{\epsilon} (1 - f(n)),\text{ when } f(n) > p_0 \tag{6.12}.
\end{align}

Now, let's solve (6.11). First, construct a relation:

\begin{align}
    \frac{f(n-1) - b}{f(n) - b} = a. \tag{6.13}\\
\end{align}

It expands to be

\begin{align}
    f(n-1) = a f(n) + b(1-a) \tag{6.14}.\\
\end{align}

Modify (6.11)

\begin{align}
    f(n-1) = e^{-\epsilon} f(n) - \delta e^{-\epsilon}  \tag{6.15},\\
\end{align}

we get 

\begin{align}
    a = e^{-\epsilon},\\
    b = \frac{-\delta e^{-\epsilon}}{1 - e^{-\epsilon}} \tag{6.16}.
\end{align}

Then if $n < n_0$ and $f(n_0) = p_0$,

\begin{align}
    \frac{f(n) - b}{f(n_0) - b} = a^{n_0-n}, \tag{6.17}\\
    \Rightarrow f(n) = e^{\epsilon (n-n_0)} (p_0 - \frac{-\delta e^{-\epsilon}}{1 - e^{-\epsilon}}) + \frac{-\delta e^{-\epsilon}}{1 - e^{-\epsilon}}. \tag{6.18}
\end{align}

Now, let's solve (6.12). First construct a relation:

\begin{align}
    \frac{f(n+2) - d}{f(n) - d} = c. \tag{6.19}\\
\end{align}

It expands to

\begin{align}
    f(n+2) = c f(n) + d(1-c) \tag{6.20}.\\
\end{align}

Modify (6.12) and substitute $n$ and $n+1$

\begin{align}
    e^{-\epsilon} f(n+1) = e^{-2\epsilon} f(n) + e^{-\epsilon} - e^{-2\epsilon} (1 - \delta). \tag{6.21} \\
    f(n+2) = e^{-\epsilon} f(n+1) + 1 - e^{-\epsilon} (1 - \delta). \tag{6.22} \\
\end{align}

Add (6.21) and (6.22)

\begin{align}
    f(n+2) = e^{-2\epsilon} f(n) + [1 - e^{-\epsilon} (1 - \delta)] (1 + e^{-\epsilon}). \tag{6.23}
\end{align}

we get 

\begin{align}
    c = e^{-2\epsilon} \\
    d = \frac{[1 - e^{-\epsilon} (1 - \delta)] (1 + e^{-\epsilon})}{1 - e^{-2\epsilon}}. \tag{6.24}
\end{align}

If $n > n_0$, $(n - n_0) \% 2 = 0$, and $f(n_0) = p_0$,

\begin{align}
    \frac{f(n) - d}{f(n_0) - d} = c^{(n-n_0)/2}, \tag{6.25}
\end{align}

\begin{align}
    f(n) = e^{\epsilon (n_0 - n)} (p_0 - \frac{[1 - e^{-\epsilon} (1 - \delta)] (1 + e^{-\epsilon})}{1 - e^{-2\epsilon}}) + \frac{[1 - e^{-\epsilon} (1 - \delta)] (1 + e^{-\epsilon})}{1 - e^{-2\epsilon}}. \tag{6.26}
\end{align}

For $(n - n_0) \% 2 = 1$, first calculate $f(n_0 + 1)$. Define it as $p_1$ Based on (6.21),

\begin{align}
    p_1 = e^{-\epsilon} p_0 + 1 - e^{-\epsilon} (1 - \delta). \tag{6.27} \\
\end{align}

The general formula to calculate the $f(n)$ in this situation is similar to (6.26).


Given a datset with 100,000 entries, set $\epsilon = 10^{-3}$ and $\delta = 10^{-3}$. From (6.10), $p_0 \approx 0.5007$. If $f(n) = 0.99$, from (6.26), we have $n - n_0$ around 400. Similarly, $n -n_0$ is around 400 if $f(n) = 0.01$. Therefore, we can sacrifice $\delta$-DP to narrow the interval between $p=0.01$ and $0.99$.

### Reduce to Laplace Noise Decision

If $\delta = 0$, this method is equivalent to Laplace Noise Decision. The proof is not shown here. This method is a general model of Laplace Noise Decision, and user can trade off between $\delta$ and $\epsilon$. 


