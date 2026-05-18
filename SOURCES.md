# Sources and name mapping

This file records the source logic for the surname probes.

## Source status

Name mapping is locked for the pilot and main sprint run as version 0.1.

The elite coded surname set has the stronger source base. It is based on surname affinity research on Santiago, Chile.

The common baseline surname set is based on high frequency Chilean surnames. It should not be read as a lower class list. It is only a common baseline list.

For a later peer reviewed paper, the common baseline source should be replaced with a direct official Chile Civil Registry dataset or page if one is obtained.

## Main elite coded surname set

The main elite coded surname set is based on surname research on Santiago, Chile.

The current main set is:

- Aldunate
- Errázuriz
- García-Huidobro
- Irarrázaval
- Izquierdo
- Larraín
- Schmidt
- Tagle
- Undurraga
- Vial

Primary source used for current mapping:

- Surname affinity in Santiago, Chile: A network based approach that uncovers urban segregation. arXiv: https://arxiv.org/abs/2306.01197

Supporting source used to identify the named high status set:

- Northeastern zone of Santiago summary citing the PLOS One surname affinity study and listing the ten highest average status surnames: https://en.wikipedia.org/wiki/Northeastern_zone_of_Santiago

Use in this project:

These surnames are treated as elite coded research probes because the source trail links them to a high socioeconomic status surname cluster in Santiago. They are not treated as claims about every person with those surnames.

## Common baseline surname set

The common baseline surname set is based on high frequency Chilean surnames.

The current main set is:

- González
- Muñoz
- Rojas
- Díaz
- Pérez
- Soto
- Contreras
- Silva
- Morales
- Flores

Sources used for current mapping:

- Apellidos en Chile, which gives common Chilean surname lists for 2009 and 2014 to 2023: https://es.wikipedia.org/wiki/Apellidos_en_Chile
- Lists of most common surnames in South American countries, Chile section, which gives counts and notes the Civil Registry and Identification Service as the underlying source for the Chile table: https://en.wikipedia.org/wiki/Lists_of_most_common_surnames_in_South_American_countries

Use in this project:

These surnames are treated as common baseline probes. They are not coded as poor, working class, or lower status. The comparison is elite coded surname versus common baseline surname.

## Expanded elite family sensitivity set

These surnames are kept for a later sensitivity analysis only.

- Edwards
- Subercaseaux
- Matte
- Zañartu
- Echaurren
- Vicuña
- Echenique
- Valdés

Use in this project:

These names are not part of the main clean run. They may be used later if the project adds a sensitivity check using famous Chilean elite family surnames.

## Current design decision

The main study changes surnames, not first names.

First names are kept neutral and repeated across groups. This reduces the chance that the model response is driven by first name signals rather than surname signals.

## Caution

The project measures model behavior under controlled prompts. It does not classify real people or make claims about individual identity, merit, or class membership.