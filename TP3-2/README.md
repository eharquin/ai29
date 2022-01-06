<h1>Exercice 2 : l'algorithme de Simon</h1>


<h2>L'algorithme :</h2>

<p>L'algorithme de Simon, contrairement à l'algorithme de Deutch-Jozsa, a été le premier algorithme quantique à montrer une accélération exponentielle par rapport au meilleur algorithme classique.</p>


<h2>Le problème :</h2>

<p>Le problème que doit résoudre l'algorithme est le suivant :

On nous donne une fonction qui fonctionne comme une boite noire.
On sait que cette fonction est soit :

- one-to-one : renvoie une unique sortie pour toute entrée. 
Exemple : $`f(1) \rightarrow 1, \quad f(2) \rightarrow 2, \quad f(3) \rightarrow 3, \quad f(4) \rightarrow 4`$

- two-to-one : renvoie une unique sortie pour strictement deux entrée différente. 
Exemple : $`f(1) \rightarrow 1, \quad f(2) \rightarrow 2, \quad f(3) \rightarrow 1, \quad f(4) \rightarrow 2`$

Cette correspondance two-to-one se fait selon une chaîne de bits secrète $`b`$ tel que :
$` \textrm{soit }x_1,x_2: \quad f(x_1) = f(x_2) \\ \textrm{on est sur que }: \quad x_1 \oplus x_2 = b `$

Le premier objectif est de déterminer si $f$ est une fonction one-to-one ou une fonction two-to-one. Si $f$ est une fonction two-to-one et le deuxième objectif est de déterminer la chaine de bits $`b`$.
Les deux cas se ramènent en réalité au même problème : trouver $`b`$, où une chaîne de bits de $`b={000...}`$ représente la fonction one-to-one de $`f`$.</p>


<h2>La solution classique :</h2>

<p>Dans le meilleur des cas si il s'agit d'une fonction two-to-one, comme pour l'algorithme de Deutch-Jozsa, seulement deux tests sont nécéssaires.

Cependant si nous voulons connaitre b pour une fonction f donné nous devrons vérifier $`2^{n-1}+1`$ entrée car nous devons tester au minimum la moitié des cas $`+1`$ jusqu'à trouver deux cas de la même sortie.

L'algorithme classique est donc de complexité $`O(2^{n-1})`$.</p>


<h2>La solution quantique :</h2>

<p>En utilisant la solution quantique il est alors possible de résoudre ce problème avec un seule appel de la fonction. Il faut cependant que la fonction soit implémenté comme un oracle quantique.</p>

<h3>Implémentation de l'algorithme quantique</h3> 

On initialise le qubit de sortie à $`|1\rangle`$:

$`\vert \psi_0 \rangle = \vert0\rangle^{\otimes n} \vert 1\rangle`$

Etape 1 : on applique la porte $H$ sur chaque qubit:

$`\vert \psi_1 \rangle = \frac{1}{\sqrt{2^{n+1}}}\sum_{x=0}^{2^n-1} \vert x\rangle \left(|0\rangle - |1 \rangle \right)`$

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

Dans cette application le gain de l’ordinateur quantique par rapport à l’ordinateur classique est impressionnant ($`1`$ seul appel contre $`2^{n-1}+1`$)

Cependant la valeur $`2^{n-1}+1`$ est un pire cas très improbable : dès qu'on rencontre deux valeurs différentes (ce qui est rapidement probable au bout de quelques appels si la fonction est équilibrée).

