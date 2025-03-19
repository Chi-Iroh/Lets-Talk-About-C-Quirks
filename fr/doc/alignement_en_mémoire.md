# L'Alignement en Mémoire

```c
struct a {
    char c;
    int n;
};

struct b {
    int n;
    char c;
};
```

## Structure a : char + int

Sur beaucoup de systèmes aujourd'hui, `char` vaut 1 octet et `int` 4 octets.  
On s'attend donc à ce que les structures `a` et `b` valent 5 octets, mais en réalité il y a de grandes chances qu'elles prennent plutôt 8 octets.  
[Un test sur 6 compilateurs C nous le montre.](https://godbolt.org/z/MqKMY8Y93)

La raison est que les données doivent être <ins>alignées</ins> en mémoire, donc que leur adresse doit être un multiple d'une puissance de 2 particulière, souvent leur taille (en octets).  
C'est pour ça que souvent, un `int` de 4 octets aura un alignement de 4 octets, donc il sera stocké à une adresse multiple de 4, comme 0, 4 ou 8, mais pas 1, 3 ou 7.  

Comme annoncé au début, il est très courant que le `char` fasse 1 octet, et l'`int` 4.  
Ainsi, le `char` prend le 1er octet, mais l'`int` doit être à une adresse multiple de 4, donc le compilateur insère 3 octets dits de "padding" (quelque chose comme "bourrage" en français) entre le `char` et l'`int` pour décaler l'`int`.  

### Mais pourquoi 3 octets ?

En effet, on a supposé qu'un `int` était à une adresse multiple de 4.  
Il se trouve qu'une structure a elle aussi un alignement, et qu'il dépend de ses champs.  
En règle générale, l'alignement d'une structure <ins>est au moins</ins> l'alignement du champ avec le plus grand alignement.  
Ici, la structure a un `int` (aligné sur 4 octets), et un `char` (aligné sur 1 octet), la structure aura un alignement d'au moins 4 octets.  

L'alignement ne pouvant être qu'une puissance de 2, si la structure a un alignement supérieur à 4, ça sera 8, 16, 32... donc des multiples de 4 (donc être aligné sur 8 octets veut aussi dire aligné sur 4 octets, mais l'inverse est faux).  
On sait donc que notre structure (et donc le `char`, puisque premier champ) sera alignée sur 4 octets.  

## Structure b : int + char

Pour la structure `b`, on vient d'établir que la structure est alignée sur au moins 4 octets, donc puisque l'`int` est le premier champ, il est forcément aligné correctement.  
Ensuite vient le char, mais puisqu'il a un alignement sur un seul octet, alors n'importe quelle adresse lui convient.  

### Mais pourquoi la structure fait 8 octets dans ce cas ?

```c
struct b b_array[2];
```
Ici on a un tableau de plusieurs structures `b`, donc si la structure fait 5 octets, pour `b[0]` tout va bien, elle commence à une adresse alignée sur 4 octets, et on vient de montrer que le `char` et l'`int` seront alignés correctement.  
Par contre, `b[0]` commence à une adresse non alignée sur 4 octets (on ajoute 5 à un multiple de 4, ça donne un multiple de 4 + 1 octet), donc le premier champ (`int`) sera mal aligné !  
On a donc un padding de 3 octets (structure de 5 octets, il manque 3 octets pour avoir 8, un multiple de 4) pour que la structure ait une taille multiple de 4, au moins si on a un tableau par exemple, on n'a plus de problèmes d'alignement.  

## Pourquoi une donnée doit être alignée ?

Pour y répondre, il faut regarder comment le processeur récupère une donnée dans la mémoire.  
Pour une donnée de plusieurs octets (en C, souvent tout sauf booléen et `char`) le processeur ne va pas lire un octet à la fois, il va lire 4 à 8 octets d'un coup (la quantité dépend de l'architecture) et les stocker dans un cache.  

Quand un programme demande d'accéder à une donnée, si elle déjà dans le cache alors tout va bien et le processeur se contente de la prendre. Sinon, on doit aller lire la RAM.  
Pour lire la RAM, on utilise des bus qui permettent de transmettre les informations nécessaires aux opérations sur la mémoire.  
Ils sont au nombre de 3 :  
1. Bus de commande : on y dépose un valeur selon s'il faut lire ou écrire des données
2. Bus d'adresse : on y dépose l'adresse à laquelle on doit effectuer la lecture/écriture
3. Bus de donnée : on y lit la donnée pour une lecture / on y dépose la donnée pour une écriture

Pour limiter la complexité des circuits électriques des bus, on ne peut lire qu'à des adresses multiples de 4 ou 8 (dépend toujours de l'architecture), d'où l'existence de l'alignement.  

Si on n'aligne pas une donnée, 2 cas :
- certains processeurs ne supportent pas les opérations sur des adresses non alignées, donc il peut y avoir un crash
- les processeurs qui gèrent ces opérations peuvent être plus lents pour l'effectuer sur une adresse non-alignée qu'alignée

Pour expliquer le 2e point, mettons un `int` de 4 octets allant de l'adresse 1 à l'adresse 4, donc prenant les 2e, 3e, 4e et 5e octets de la mémoire.  
Le processeur demande aux bus de lire les 4 premiers octets de la mémoire, donc du 1er au 4e, il nous manque donc le 5e octet.  
Pour le récupérer, le processeur demande encore aux bus de lire de la mémoire, cette fois à partir de 5e octet.  
Il nous a donc fallu 2 opérations de lectures pour lire une donnée qui pouvait être lue en une fois si elle était alignée, donc ça peut dégrader les performances.  

Cependant, cette réduction des performances est aujourd'hui plus faible qu'autrefois.  

## Sources :

https://en.wikipedia.org/wiki/Data_structure_alignment  
https://stackoverflow.com/questions/4306186/structure-padding-and-packing  
http://www.catb.org/esr/structure-packing/  
https://stackoverflow.com/questions/41251388/why-processor-read-only-aligned-addresses  
https://www.reddit.com/r/osdev/comments/wwnl54/why_are_cache_line_accesses_aligned/  
https://lemire.me/blog/2012/05/31/data-alignment-for-speed-myth-or-reality/  
