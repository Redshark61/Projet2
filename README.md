# projet2

- [Spécificités techniques](#specificites-techniques)

## Français

### Spécificités techniques

#### Créer une nouvelle map

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
    ], entityData=[])
    ```

    Les paramètres sont dans l'ordre:

  1. Le chemin du monde d'où l'on vient
  1. Le chemin du monde vers lequel on va
  1. La collision qui permet de rentrer dans le monde
  1. Le point de spawn du joueur

- Donjon :
