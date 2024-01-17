# GNS3_Project - Telnet Implementation

Groupe 26,
Membres :
1. Maxence Poisse-Joubert
2. Hélio Vatan


# Instructions

## Network_Intent

The file is organised via lists, with each list containing dictionnaries which contains attributes in the form of keys. The main lists are "routers" and "AS" and are implemented as such :

### Routers 
List of different dictionnaries representing one router and it's multiple caracteristics.

1. "ID" - Is a list containing :
  - A unique, strictly positive integer, used to identify the router in the programm. This number should correspond to the position of the router in the list (if we start counting by one).
  - A string corresponding to the hostname (The hostname does not need to be unique to the router, it is only recommended to have unique names).

2. "AS" :

  - A strictly positive integer, represents the AS of the router _(The AS needs to exist in the AS list)_

3. "interface" - A list containing :
  - A list of the ID of the router(s) connected to an interface _(the program currently only accepts one connected router per interface)_
  - A string representing the interface name in the router environnement

4. "Port" : 
  - A integer which correspond to the port given by GNS3 to the router

### AS
List of dictionnaries representing the AS(s) in the Network.

1. "ASName"
  - A strictly positive integer corresponding to the AS number

2. "networkIP" - A list containing two strings :
  - The AS network ipv6 address without the mask
  - The AS network ipv6 mask

3. "loopbackNetworkIP" - A list containing two strings :
  - The AS loopback network ipv6 address without the mask
  - The AS loopback network ipv6 mask

4. "IGP" 
- A list containing as many strings as Interior Gateway Protocols in the AS, for the now the possible values are :

  -- "RIP", "OSPF"

### Constants

A dictonnary of dictionnaries referencing different constants and norms for every routers / AS

1. "Bandwith" - Contains the reference bandwith and the bandwith of the various interfaces, used in OSPF metrics
  - Values must be integers, unit is the kilobyte for interfaces and megabytes for reference (Used by the GNS3 terminals by default)

## How to use 

Setup the network on GNS3 according to the network intent. Before executing the program, you must have the network started, as well as a console opened on every router.
