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

<h3>Implémentation de l'algorithme quantique avec 3 qubit</h3> 

L'algorithme utilise un oracle quantique boite noire qui prend en entrée une chaine de 3 bits.

Code:

```python
b = '110'

n = len(b)
simon_circuit = QuantumCircuit(n*2, n)

# Apply Hadamard gates before querying the oracle
simon_circuit.h(range(n))    
    
# Apply barrier for visual separation
simon_circuit.barrier()

simon_circuit += simon_oracle(b)

# Apply barrier for visual separation
simon_circuit.barrier()

# Apply Hadamard gates to the input register
simon_circuit.h(range(n))

# Measure qubits
simon_circuit.measure(range(n), range(n))
simon_circuit.draw()
```

Circuit :

```text
     ┌───┐ ░                           ░ ┌───┐┌─┐
q_0: ┤ H ├─░───■───────────────────────░─┤ H ├┤M├──────
     ├───┤ ░   │                       ░ ├───┤└╥┘┌─┐
q_1: ┤ H ├─░───┼────■─────────■────■───░─┤ H ├─╫─┤M├───
     ├───┤ ░   │    │         │    │   ░ ├───┤ ║ └╥┘┌─┐
q_2: ┤ H ├─░───┼────┼────■────┼────┼───░─┤ H ├─╫──╫─┤M├
     └───┘ ░ ┌─┴─┐  │    │    │    │   ░ └───┘ ║  ║ └╥┘
q_3: ──────░─┤ X ├──┼────┼────┼────┼───░───────╫──╫──╫─
           ░ └───┘┌─┴─┐  │  ┌─┴─┐  │   ░       ║  ║  ║
q_4: ──────░──────┤ X ├──┼──┤ X ├──┼───░───────╫──╫──╫─
           ░      └───┘┌─┴─┐└───┘┌─┴─┐ ░       ║  ║  ║
q_5: ──────░───────────┤ X ├─────┤ X ├─░───────╫──╫──╫─
           ░           └───┘     └───┘ ░       ║  ║  ║
c: 3/══════════════════════════════════════════╩══╩══╩═
                                               0  1  2
```

En utilisant un simulateur on peut facilement vérifier qu'on peut retrouver la valeur de la chaine de bit b en résolvant un système d'équation. Ici l'algorithme quantique résout les équations simultanément.

Par exemple si on mesure $`001`$ dans un premier temps, on a:

$`\begin{aligned} b \cdot 001 &= 0 \\ (b_2 \cdot 0) + (b_1 \cdot 0) + (b_0 \cdot 1) & = 0 \\ (\cancel{b_2 \cdot 0}) + (\cancel{b_1 \cdot 0}) + (b_0 \cdot 1) & = 0 \\ b_0 & = 0\\ \end{aligned} `$

Et si dans un second temps on mesure $`111`$ :

$`\begin{aligned} b \cdot 111 &= 0 \\ (b_2 \cdot 1) + (b_1 \cdot 1) + (\cancel{0 \cdot 1}) & = 0 \\ (b_2 \cdot 1) + (b_1 \cdot 1) & = 0 \\ \end{aligned} `$

On peut donc retrouver la chaine de bit progressivement. 
Ici on sait que b vaut soit $`000`$ ou $`110`$.



<h2>Consclusion</h2>

Contrairement à l'algorithme de Deutch-Jozsa, l'algorithme de simon montre une accélération exponentielle par rapport au meilleur algorithme classique que nous pouvons produire.</p>

Dans cette application le gain de l’ordinateur quantique par rapport à l’ordinateur classique est impressionnant ($`O(n)`$ contre $`O(2^{n-1})`$)
