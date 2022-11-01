# PokemonDatabase

## Preview
Link to video of database in action: https://youtu.be/V7IKl0XaLqA

## ER DIAGRAM

![ERDIAGRAM](pokemon.png)

### Summary of Database:
 |Table Name|Cardinality|Arity|
|-------------------|--------------:|--------------:|
|Ability|326|4|
|Areas|702|3|
|EggGroup|15|2|
|EncounterMethod|19|2|
|EncounterSlot|560|5|
|Forms|395|14|
|FormType|531|3|
|Generation|8|3|
|Items|1607|7|
|LearnMethod|11|2|
|Locations|796|3|
|Machine|1688|4|
|Moves|844|11|
|PkmnAbilities|2143|4|
|PkmnAreaVrsEncntr|219|4|
|PkmnEggGroup|1154|2|
|PkmnHeldItemVrsn|5002|4|
|PkmnVrsnMoveLrn|478741|4|
|Pokemon|898|25|
|PokemonForm|360|2|
|PokemonType|1340|3|
|Regions|8|3|
|RegularEvolution|429|14|
|TypeDamageRelation|324|3|
|Types|20|3|
|UniqueEvolution|16|8|
|Version|34|3|
|VersionGroup|20|3|


###List of of Sample Queries:

One of the constraints of the project was that users are not allowed to freely enter SQL commands. So, these queries are hardcoded and can be returned by pressing buttons.
```python

1. Heaviest Pokemon 

  a. This query returns the 5 heaviest base Pokemon (not including the Forms)
  
2. Base Pokemon with highest stats

  a. This query returns 5 Pokemon with the highest stats (not including Forms)
  
3. Type with most moves

  a. This query returns a list of types and the number of moves under that type in descending order. 
  
4. Find the number of moves a Pokemon with a name starting with the letter “B” in each version group. 

  a. I. e. , it will return the number of moves:
  
    i. Bulbasaur can learn in version groups 1 to 20. 
    
    ii. Blastoise can learn in version groups 1 to 20. 
    
5. Find legendary Pokemon that can evolve

  a. This returns all the legendary Pokemon that can evolve
  
6. Pokemon that can have more than 2 possible abilities

  a. This returns the Pokemon ID of all Pokemon that can have more than 2 possible abilities.  This includes hidden abilities. 
  
  b. For example: Venomoth can have either Shield Dust or Tinted Lens, or Wonder skin (hidden ability)
  
7. Distribution of Pokemon types per region

  a. Returns the distribution of Pokemon types for each region.  Note that Kanto is poisonous as hell. 
  
8. Palindrome Names

  a. Returns all Pokemon with palindrome names. 
  
  b. For example: eevee and ho-oh
  
9. Pokemon with no evolution line

  a. Returns all Pokemon that are not part of an evolution family (i. e, doesn’t evolve)
  
  b. In addition, legendary and mythical Pokemon are excluded as most of them do not evolve anyway. 
  
  c. Finally, for our purposes, regional form evolutions are counted. 
  
10. Average height of all egg groups
```

Sources:

PokeAPI: 	https://pokeapi.co/

Veekun:		https://github.com/veekun/pokedex
