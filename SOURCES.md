# Sources and name mapping

This file records the current source logic for the surname probes.

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

Source used for current mapping:

- Surname affinity networks uncover population structure. arXiv version: https://arxiv.org/abs/2306.01197
- The same research line appears in PLOS One work on surname affinity networks and population structure in Santiago, Chile.

Use in this project:

These surnames are treated as elite coded research probes because the source links them to a high socioeconomic status cluster in Santiago. They are not treated as claims about every person with those surnames.

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

Source used for current mapping:

- Apellidos en Chile: https://es.wikipedia.org/wiki/Apellidos_en_Chile

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