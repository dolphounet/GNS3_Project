# GNS3_Project

Groupe 26,
Membres :
1. Maxence Poisse-Joubert
2. Hélio Vatan


# Instructions

## Network_Intent

The file is organised via lists, with each list containing dictionnaries which contains attributes in the form of keys. The main lists are "routers" and "AS" and are implemented as such :

###Routers - List of different dictionnaries representing one router and it's multiple caracteristics.

1. "ID" :

Is a list containing :
- A unique positive integer (except 0) used to identify the router in the programm. This number should correspond to the position of the router in the list (if we start counting by one).
- A string corresponding to the hostname (The hostname does not need to be unique to the router).

2. "AS" :

- A positive integer superior to zero, represents the AS of the router _(The AS needs to exist in the AS list)_

3. "interface" :

Is a list with two values, 
- A list of the ID of the router(s) connected to an interface _(the program currently only accepts one connected router per interface)_
- A string representing the interface name in the router environnement