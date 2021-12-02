# projet2

- [Créer une nouvelle map](#creer-une-nouvelle-map)

## Français

### Créer une nouvelle map

- Overworld :

    Dans le fichier `map.py` de votre projet, ajouter la ligne suivante dans le init :

    ```python
            self.registerMap("1", portals=[], entityData=[], spawnName="")
    ```

    Dans le `1` il faut mettre le chemin vers le fichier `tmx` de votre map à partir du dossier asset. Par exemple pour une carte dans `assets/monde/monde.tmx` vous allez mettre `monde/monde`.

    ---
    Pour le **paramètre portal**, il faut mettre une instance de `Portal` pour chaque portail vers un autre monde.

    *Exemple* : un portail qui part du `monde 2`, vers le `monde 3`, quand le joueur rentre dans la collision `toMonde3`, et apparaît au point de spawn `spawnPlayer`. On écrira donc :

    ```python
    self.registerMap("monde 2/monde 2", portals=[
        Portal("monde 2/monde 2", "monde 3/monde 3", "toMonde3", "spawnPlayer")
    ], entityData=[], spawnName="")
    ```

    Les paramètres sont dans l'ordre:

  1. Le chemin du monde d'où l'on vient
  2. Le chemin du monde vers lequel on va
  3. La collision qui permet de rentrer dans le monde
  4. Le point de spawn du joueur

  **IMPORTANT :** il faut qu'il y ait de le mot *donjon* dans le nom de votre map si c'est un donjon.

  ---
  Pour le **paramètre entityData**, il faut mettre une liste d'instance de `Monstre` à créer.
  
  Si aucun monstre ne doit être créé, mettre une liste vide.
  
  Par exemple :

  ```python
  entityData = [
    Monster("Monsters/Demons/RedDemon", xp=30, speed=(50, 60)),
    Monster("Monsters/Orcs/Orc", xp=50, health=200, speed=(20, 30)),
  ]
  ```

  Paramètres :
  1. *Chemin* qui mène au PNG du monstre (en partant de assets/Characters).
  2. *Nombre d'expérience* que le monstre donne quand il meurt.
  3. *Vitesse* du monstre (aléatoire entre les deux valeurs). *Maximum 100*
  4. Enfin le paramètre *health* est optionnel, si il n'est pas précisé, le monstre a 100pv.

  ---
  Pour le **paramètre spawnName**, il faut mettre le nom du point de spawn des monstres.

  Laisser une string vide si aucun monstre ne doit spawner.
  
  **Ce nom doit être différent pour chaque donjon !**

  *Exemple* :

  ```python
        self.registerMap("assetAir/donjon/donjon",
                        portals=[Portal("assetAir/donjon/donjon", "assetAir/airWorld", "toAir", "spawnPlayer")],
                        entityData=[
                            Monster("Monsters/Demons/RedDemon", xp=30, speed=(50, 60)),
                            Monster("Monsters/Orcs/Orc", xp=50, health=200, speed=(20, 30)),
                        ],
                        spawnName="AirSpawnMonster")
  ```
