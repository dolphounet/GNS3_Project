# Configuration Générale

## Une fois par routeur
Router(config)# ipv6 unicast-routing
## Pour toutes les interfaces
Router(config)# interface _interface name_
Router(config-if)# ipv6 enable
Router(config-if)# ipv6 address _ipv6-address_/_prefix-length_
Router(config-if)# no shutdown
# Configuration RIP

Router(config)# ipv6 router rip _process name_
Router(config-rtr)# redistribute connected

Router(config-if)# ipv6 rip process name enable //Pour toutes les interfaces où activer RIP

# Configuration OSPF

Router(config)# ipv6 router ospf _process-id_
Router(config-rtr)# router-id _router-id_
Router(config)# interface _interface name_
Router(config-if)# ipv6 ospf _process-id_ area _area-id_
# Configuration BGP

Router(config)# router bgp _as-number_
Router(config-router)# no bgp default ipv4-unicast$
Device(config-router)# bgp router-id _X.X.X.X_
## Pour établir la session entre deux voisins
Router(config-router)# neighbor _ipv6-address_ remote-as _as-number_
Router(config-router)# address-family ipv6 unicast
Router(config-router-af)# neighbor _ipv6-address_ activate
## Pour advertise des routes
Router(config-router)# address-family ipv6 unicast
Router(config-router-af)# network _ipv6-prefix_

## Filtres
### Création de filtres
#### On crée une access-list
Router(config)# ipv6 access-list _name-acl_
Router(config-ipv6-acl)# {permit|deny} _ipv6-source-prefix_ _ipv6-dest-prefix_
#### On l'applique à une route-map
Router(config)# route-map _map-tag_ {permit|deny} _sequence-number_
Router(config-route-map)# match ipv6 address _name-acl_
#### On applique la route-map à un voisin
Router(config-router-af)# neighbor _ipv6-address_ route-map _map-tag_ {in|out}
### Local preference
Router(config-route-map)# set local-preference _local_preference_value_
### AS path prepending
Router(config-route-map)# set as-path prepend x*_YOUR_AS_NUMBER_

### Test GitHub
