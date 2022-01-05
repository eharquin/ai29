<h1>Exercice 1 : l'algorithme de Deutch-Jozsa</h1>


<h2>L'algorithme :</h2>

<p>L'algorithme de Deutsch-Jozsa, a été le premier exemple d'un algorithme quantique dont les performances se sont montrés supérieures à celles du meilleur algorithme classique. Il a montré pour la première vfois que l'utilisation d'un ordinateur quantique pouvait, dans certains usages, dépasser les ordianteurs classiques.</p>


<h2>Le problème :</h2>

<p>Le problème que doit résoudre l'algorithme est le suivant :

On nous donne une fonction booléenne qui fonctionne comme une boite noire.
Cette fonction prend en entrée une chaine de bit et renvoie soit $`0`$ ou $`1`$.

On sait que la fonction est forcément soit constante soit équilibrée.

Une fonction constante renvoie toujours $`0`$ ou alors toujours $`1`$ peut importe son entrée. Une fonction équilibré renvoie dans 50% des cas $0$ et dans 50% des cas $1$.

L'objectif est de determiné si une fonction donné est constante ou équilibré.</p>


<h2>La solution classique :</h2>

<p>Dans le meilleur des cas seulement deux tests sont nécéssaire : si la première sortie est $`1`$ et la deuxième est $`0`$ on peut être sur que la fonction est équilibrée.

Dans le pire cas la solution classique mettra $`2^{n-1}+1`$ car nous devons tester au minimum la moitié des cas $`+1`$ pour s'assurer que la fonction est bien constante.

L'algorithme classique est donc de complexité $`O(2^{n-1})`$.</p>


<h2>La solution quantique :</h2>

<p>En utilisant la solution quantique il est alors possible de résoudre ce problème avec un seule appel de la fonction. Il faut cependant que la fonction soit implémenté comme un oracle quantique.</p>

<h3>Implémentation des oracles quantique</h3> 

<p>Pour l'oracle constant c'est très simple :

Si $`f(x) = 0`$, alors on applique la porte $`I`$ sur le deuxième qubit.

Si $`f(x) = 1`$, alors on applique la porte $`X`$ sur le deuxième qubit.

Et inversement si on veut une fonction constante qui retourne $`1`$.

Ci-dessous le code permetant d'implémenter l'oracle constant:
```python
n = 3

const_oracle = QuantumCircuit(n+1)

output = np.random.randint(2)
if output == 1:
    const_oracle.x(n)

const_oracle.draw()
```

Dans ce cas l'entrée n'a pas d'effet sur la sortie donc on fixe aléatoirement le qubit de sortie à $`|0\rangle`$ ou $`|1\rangle`$.

Le circuit quand le troisième qubit est fixé à $`|0\rangle`$:

```
q_0: ─────

q_1: ─────

q_2: ─────

q_3: ─────

```

Le circuit quand le troisième qubit est fixé à $`|1\rangle`$:

```
q_0: ─────

q_1: ─────

q_2: ─────
     ┌───┐
q_3: ┤ X ├
     └───┘
```

Pour l'oracle équilibré ça se complique un peu et il existe différentes implémentation du circuit, le site de quiskit propose l'implémentation suivante:
```python
n = 3

balanced_oracle = QuantumCircuit(n+1)
b_str = "101"

# Place X-gates
for qubit in range(len(b_str)):
    if b_str[qubit] == '1':
        balanced_oracle.x(qubit)

# Use barrier as divider
balanced_oracle.barrier()

# Controlled-NOT gates
for qubit in range(n):
    balanced_oracle.cx(qubit, n)

balanced_oracle.barrier()

# Place X-gates
for qubit in range(len(b_str)):
    if b_str[qubit] == '1':
        balanced_oracle.x(qubit)

# Show oracle
balanced_oracle.draw()
```

Pour commencer on définit une chaine de bit qui initialise les qubits en appliquant des portes $`X`$ quand il s'agit d'un $`|1\rangle`$.

Ensuite, on ajoute des portes C-NOT en utilisant chaque qubit d'entrée comme contrôle, et le qubit de sortie comme cible.

Pour finir on réapplique à nouveau les portes $X$ de la première étape pour restaurer l'état des qubits.
</p>


<h3>Implémentation de l'algorithme quantique</h3> 

On initialise le qubit de sortie à $|1\rangle$:

$$\vert \psi_0 \rangle = \vert0\rangle^{\otimes n} \vert 1\rangle$$

Etape 1 : on applique la porte $H$ sur chaque qubit:

$$\vert \psi_1 \rangle = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1} \vert x\rangle \left(|0\rangle - |1 \rangle \right)$$

Code :
```python
n = 3

dj_circuit = QuantumCircuit(n+1, n)

# Apply H-gates
for qubit in range(n):
    dj_circuit.h(qubit)

# Put qubit in state |->
dj_circuit.x(n)
dj_circuit.h(n)
dj_circuit.draw()
```
Circuit :
```text
     ┌───┐
q_0: ┤ H ├─────
     ├───┤
q_1: ┤ H ├─────
     ├───┤
q_2: ┤ H ├─────
     ├───┤┌───┐
q_3: ┤ X ├┤ H ├
     └───┘└───┘
c: 3/══════════
```

Maintenant on ajoute l'oracle, par exemple l'oracle équilibrée :

Code :
```python
n = 3

dj_circuit = QuantumCircuit(n+1, n)

# Apply H-gates
for qubit in range(n):
    dj_circuit.h(qubit)

# Put qubit in state |->
dj_circuit.x(n)
dj_circuit.h(n)

# Add oracle
dj_circuit += balanced_oracle
dj_circuit.draw()
```

Circuit :

```text
     ┌───┐┌───┐ ░                 ░ ┌───┐
q_0: ┤ H ├┤ X ├─░───■─────────────░─┤ X ├
     ├───┤└───┘ ░   │             ░ └───┘
q_1: ┤ H ├──────░───┼────■────────░──────
     ├───┤┌───┐ ░   │    │        ░ ┌───┐
q_2: ┤ H ├┤ X ├─░───┼────┼────■───░─┤ X ├
     ├───┤├───┤ ░ ┌─┴─┐┌─┴─┐┌─┴─┐ ░ └───┘
q_3: ┤ X ├┤ H ├─░─┤ X ├┤ X ├┤ X ├─░──────
     └───┘└───┘ ░ └───┘└───┘└───┘ ░
c: 3/════════════════════════════════════

```

Pour finir on applique des porte $H$ sur nos qubit d'entrée et on les mesures :

```python
n = 3

dj_circuit = QuantumCircuit(n+1, n)

# Apply H-gates
for qubit in range(n):
    dj_circuit.h(qubit)

# Put qubit in state |->
dj_circuit.x(n)
dj_circuit.h(n)

# Add oracle
dj_circuit += balanced_oracle

# Repeat H-gates
for qubit in range(n):
    dj_circuit.h(qubit)
dj_circuit.barrier()

# Measure
for i in range(n):
    dj_circuit.measure(i, i)

# Display circuit
dj_circuit.draw()
```



Pour commencer décomposons les étapes de l'algorithme:

```text
      | ┌───┐ | ┌───┐ ░                 ░ ┌───┐ ░ ┌─┐      
q_0: ─|─┤ H ├─|─┤ X ├─░───■─────────────░─┤ H ├─░─┤M├──────
      | ├───┤ | └───┘ ░   │             ░ ├───┤ ░ └╥┘┌─┐   
q_1: ─|─┤ H ├─|───────░───┼────■────────░─┤ H ├─░──╫─┤M├───
      | ├───┤ | ┌───┐ ░   │    │        ░ ├───┤ ░  ║ └╥┘┌─┐
q_2: ─|─┤ H ├─|─┤ X ├─░───┼────┼────■───░─┤ H ├─░──╫──╫─┤M├
      | ├───┤ | ├───┤ ░ ┌─┴─┐┌─┴─┐┌─┴─┐ ░ └───┘ ░  ║  ║ └╥┘
q_3: ─|─┤ X ├─|─┤ H ├─░─┤ X ├┤ X ├┤ X ├─░───────░──╫──╫──╫─
      | └───┘ | └───┘ ░ └───┘└───┘└───┘ ░       ░  ║  ║  ║ 
c: 3/═|═══════|════════════════════════════════════╩══╩══╩═
      |       |                                    0  1  2 
      |       |
      0       0
```

On commence par préparer deux registres quantique, le premier est un $n$-qubit registre initialisé à $|0\rangle$, et le deuxième est-un registre quantique à un qubit initialisé à $|1\rangle$: $$\vert \psi_0 \rangle = \vert0\rangle^{\otimes n} \vert 1\rangle$$


Apply a Hadamard gate to each qubit: $$\vert \psi_1 \rangle = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1} \vert x\rangle \left(|0\rangle - |1 \rangle \right)$$
Apply the quantum oracle $\vert x\rangle \vert y\rangle$ to $\vert x\rangle \vert y \oplus f(x)\rangle$: $$ \begin{aligned} \lvert \psi_2 \rangle & = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1} \vert x\rangle (\vert f(x)\rangle - \vert 1 \oplus f(x)\rangle) \\ & = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1}(-1)^{f(x)}|x\rangle ( |0\rangle - |1\rangle ) \end{aligned} $$ since for each $x,f(x)$ is either $0$ or $1$.
At this point the second single qubit register may be ignored. Apply a Hadamard gate to each qubit in the first register: $$ \begin{aligned} \lvert \psi_3 \rangle & = \frac{1}{2^n}\sum_{x=0}^{2^n-1}(-1)^{f(x)} \left[ \sum_{y=0}^{2^n-1}(-1)^{x \cdot y} \vert y \rangle \right] \\ & = \frac{1}{2^n}\sum_{y=0}^{2^n-1} \left[ \sum_{x=0}^{2^n-1}(-1)^{f(x)}(-1)^{x \cdot y} \right] \vert y \rangle \end{aligned} $$ where $x \cdot y = x_0y_0 \oplus x_1y_1 \oplus \ldots \oplus x_{n-1}y_{n-1}$ is the sum of the bitwise product.
Measure the first register. Notice that the probability of measuring $\vert 0 \rangle ^{\otimes n} = \lvert \frac{1}{2^n}\sum_{x=0}^{2^n-1}(-1)^{f(x)} \rvert^2$, which evaluates to $1$ if $f(x)$ is constant and $0$ if $f(x)$ is balanced.


1.4 Why Does This Work?
Constant Oracle
When the oracle is constant, it has no effect (up to a global phase) on the input qubits, and the quantum states before and after querying the oracle are the same. Since the H-gate is its own inverse, in Step 4 we reverse Step 2 to obtain the initial quantum state of $|00\dots 0\rangle$ in the first register.

$$ H^{\otimes n}\begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \end{bmatrix} = \tfrac{1}{\sqrt{2^n}}\begin{bmatrix} 1 \\ 1 \\ 1 \\ \vdots \\ 1 \end{bmatrix} \quad \xrightarrow{\text{after } U_f} \quad H^{\otimes n}\tfrac{1}{\sqrt{2^n}}\begin{bmatrix} 1 \\ 1 \\ 1 \\ \vdots \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \\ 0 \\ \vdots \\ 0 \end{bmatrix} $$
Balanced Oracle
After step 2, our input register is an equal superposition of all the states in the computational basis. When the oracle is balanced, phase kickback adds a negative phase to exactly half these states:

$$ U_f \tfrac{1}{\sqrt{2^n}}\begin{bmatrix} 1 \\ 1 \\ 1 \\ \vdots \\ 1 \end{bmatrix} = \tfrac{1}{\sqrt{2^n}}\begin{bmatrix} -1 \\ 1 \\ -1 \\ \vdots \\ 1 \end{bmatrix} $$
The quantum state after querying the oracle is orthogonal to the quantum state before querying the oracle. Thus, in Step 4, when applying the H-gates, we must end up with a quantum state that is orthogonal to $|00\dots 0\rangle$. This means we should never measure the all-zero state.

2. Worked Example
Let's go through a specific example for a two bit balanced function:

Consider a two-bit function $f(x_0,x_1)=x_0 \oplus x_1$ such that

$f(0,0)=0$

$f(0,1)=1$

$f(1,0)=1$

$f(1,1)=0$

The corresponding phase oracle of this two-bit oralce is $U_f \lvert x_1, x_0 \rangle = (-1)^{f(x_1, x_0)}\lvert x \rangle$

We will now check if this oracle works as expected by taking a example state $$\lvert \psi_0 \rangle = \lvert 0 0 \rangle_{01} \otimes \lvert 1 \rangle_{2} $$

The first register of two qubits is initialized to $|00\rangle$ and the second register qubit to $|1\rangle$ (Note that we are using subscripts 0, 1, and 2 to index the qubits. A subscript of "01" indicates the state of the register containing qubits 0 and 1) $$\lvert \psi_0 \rangle = \lvert 0 0 \rangle_{01} \otimes \lvert 1 \rangle_{2} $$
Apply Hadamard on all qubits $$\lvert \psi_1 \rangle = \frac{1}{2} \left( \lvert 0 0 \rangle + \lvert 0 1 \rangle + \lvert 1 0 \rangle + \lvert 1 1 \rangle \right)_{01} \otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} $$
The oracle function can be implemented as $\text{Q}_f = CX_{02}CX_{12}$, $$ \begin{align*} \lvert \psi_2 \rangle = \frac{1}{2\sqrt{2}} \left[ \lvert 0 0 \rangle_{01} \otimes \left( \lvert 0 \oplus 0 \oplus 0 \rangle - \lvert 1 \oplus 0 \oplus 0 \rangle \right)_{2} \\ + \lvert 0 1 \rangle_{01} \otimes \left( \lvert 0 \oplus 0 \oplus 1 \rangle - \lvert 1 \oplus 0 \oplus 1 \rangle \right)_{2} \\ + \lvert 1 0 \rangle_{01} \otimes \left( \lvert 0 \oplus 1 \oplus 0 \rangle - \lvert 1 \oplus 1 \oplus 0 \rangle \right)_{2} \\ + \lvert 1 1 \rangle_{01} \otimes \left( \lvert 0 \oplus 1 \oplus 1 \rangle - \lvert 1 \oplus 1 \oplus 1 \rangle \right)_{2} \right] \end{align*} $$
Simplifying this, we get the following: $$ \begin{aligned} \lvert \psi_2 \rangle & = \frac{1}{2\sqrt{2}} \left[ \lvert 0 0 \rangle_{01} \otimes \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} - \lvert 0 1 \rangle_{01} \otimes \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} - \lvert 1 0 \rangle_{01} \otimes \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} + \lvert 1 1 \rangle_{01} \otimes \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} \right] \\ & = \frac{1}{2} \left( \lvert 0 0 \rangle - \lvert 0 1 \rangle - \lvert 1 0 \rangle + \lvert 1 1 \rangle \right)_{01} \otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} \\ & = \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{0} \otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{1} \otimes \frac{1}{\sqrt{2}} \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} \end{aligned} $$
Apply Hadamard on the first register $$ \lvert \psi_3\rangle = \lvert 1 \rangle_{0} \otimes \lvert 1 \rangle_{1} \otimes \left( \lvert 0 \rangle - \lvert 1 \rangle \right)_{2} $$
Measuring the first two qubits will give the non-zero $11$, indicating a balanced function.
You can try out similar examples using the widget below. Press the buttons to add H-gates and oracles, re-run the cell and/or set case="constant" to try out different oracles.

3. Creating Quantum Oracles
Let's see some different ways we can create a quantum oracle.

For a constant function, it is simple:

$\qquad$ 1. if f(x) = 0, then apply the $I$ gate to the qubit in register 2.
$\qquad$ 2. if f(x) = 1, then apply the $X$ gate to the qubit in register 2.

For a balanced function, there are many different circuits we can create. One of the ways we can guarantee our circuit is balanced is by performing a CNOT for each qubit in register 1, with the qubit in register 2 as the target. For example:
