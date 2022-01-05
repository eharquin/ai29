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

On initialise le qubit de sortie à $`|1\rangle`$:

$$`\vert \psi_0 \rangle = \vert0\rangle^{\otimes n} \vert 1\rangle`$$

Etape 1 : on applique la porte $H$ sur chaque qubit:

$$`\vert \psi_1 \rangle = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1} \vert x\rangle \left(|0\rangle - |1 \rangle \right)`$$

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

Pour finir on applique des porte $`H`$ sur nos qubit d'entrée et on les mesures :

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

<h2>Consclusion</h2>

Dans le cas de l'oracle équilibrée en mesurant on constate qu'on a 0% de chance de mesurer 000 et 100% de chance de mesurer 111 ce qui prédit correctement que la fonction est balancée.

Dans cette application le gain de l’ordinateur quantique par rapport à l’ordinateur classique est impressionnant ($1$ seul appel contre $2^{n-1}+1$)

Cependant la valeur $2^{n-1}+1$ est un pire cas très improbable : dès qu'on rencontre deux valeurs différentes (ce qui est rapidement probable au bout de quelques appels si la fonction est équilibrée).