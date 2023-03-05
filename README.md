# PLY_SC1

> Auteurs : ***James ABIB*** et ***Ronan KIELT***

## Installation

  *  Installer requirements.txt avec la commande `pip install -r requirements.txt`

  *  Installer graphviz avec la commande `sudo apt-get install graphviz` (linux) ou `brew install graphviz` (pour mac) ou `choco install graphviz` (pour windows)


## Fonctionnalités

1. Noms de variables à plusieurs caractères

2. Affectation dans une variable : 
```c
x=2;
x=2+2;
x= "Hello World";
```

3. Affichage d’expressions numériques (pouvant contenir des variables numériques) : 
```c++
x=2;
print(x+2);
print(2+2);
```

4. Instructions conditionnelles :
```c++
x=2;
if (x>2) { print(x+2); } else { print(x-2); }
if (x>2) { print(x+2); } else if (x<2) { print(x-2); } else { print(x); }
if (x>2) { print(x+2); } elif (x<2) { print(x-2); } else { print(x); }
```

5. Structures itératives (while et for) :
```c++
x=2;
while (x<10) { print(x); x=x+1; }
for (i=0; i<10; i=i+1) { print(i); }
```

6. Affichage de l’arbre de syntaxe (sur la console ou avec graphViz)

7. Gérer les fonctions avec/sans paramètre sans valeur de retour :
```php
function f() { print(2); }
function f(x) { print(x); }
function f(x, y) { print(x+y); }
```

8. Les tableaux :
```c++
x = [1, 2, 3];
y = [1, 2, 3, 4, 5];
z = [1, 2, 3, 4, 5, 6, 7, 8, 9];
print(x[0]);
print(y[1]);
print(z[2]);
print(x[0] + y[1] + z[2]);
```	
9. Gestion des erreurs (variable non initialisée, ...)

10. String et affichage de String
```c++
x = "Hello World";
print(x);

y = "Hello";
z = "World";
print(y + " " + z);
print("Hello" + " " + "World");
print("Hello World");
```

11. Incrémentation et affectation élargie :
```c++
x++; 
x--;
x+=1;
x-=1;
x/=1;
x*=1;
```

12. Commentaires :
```c++
// commentaire sur une ligne
/* commentaire sur 
plusieurs lignes */
```

## Fonctionnalités non implémentées

13. Comparaison multiples à la python :
```c++
1<2<3
```

14. Déclaration explicite des variables :
```c#	
x;
y;
z;
```
15.  Fonctions avec valeur de retour
```php
function comparaison(c) {
  if(c==1) {
    return 0;
  }
  return 1;
}
```

16. Scope des variables

17. Fonctions récursives terminales

18. Programmation Orienté Objet

19. Passage des paramètres par référence (cf id() en python)

20. Variables globales
21. Affectations multiples :
```python
a,b,c = 2,3,5;
```
22. Print multiples :
```c++
print(x+2, "toto");
```

23. Génération automatique d’une docString
