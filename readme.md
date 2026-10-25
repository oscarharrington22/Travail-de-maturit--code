# Tutorapp

Tutorapp a pour but de permettre aux élèves cherchant un répétiteur pour des cours d’appui d’en trouver un correspondant à leurs besoins.

C’est également une plateforme permettant à ceux qui souhaitent donner des cours de se créer un profil et d’être trouvés par des élèves à la recherche d’aide dans une matière.

## Fonctionnalités

- **Gestion de compte :**

À l’inscription ou bien plus tard, les utilisateurs peuvent cocher une case indiquant s’ils souhaitent donner ou non des cours. Les utilisateurs listés comme pouvant donner des cours remplissent un formulaire spécifique avec les informations nécessaires à leur profil de répétiteur, qu’ils pourront facilement modifier par la suite s'ils le souhaitent.

- **Recherche de répétiteurs :**

La principale fonctionnalité de Tutorapp est la recherche d’un répétiteur adéquat à l’aide de plusieurs filtres. Les élèves peuvent utiliser différents filtres pour trouver un répétiteur correspondant à leurs besoins, notamment en fonction de la matière, du tarif, du niveau d’études, de la ville et des disponibilités.

- **Demandes de leçon :**

Une fois qu’un élève a trouvé un répétiteur qui correspond à ses besoins, il peut lui envoyer une demande de leçon. L’élève peut indiquer la matière, ainsi que la date et l’heure souhaitées. Le répétiteur peut ensuite consulter les demandes qu’il reçoit et les accepter ou les refuser. Les demandes peuvent également être ponctuelles ou se répéter régulièrement selon les besoins de l’élève.

- **Disponibilités :**

Les répétiteurs peuvent informer de leurs disponibilités en indiquant les jours et les heures auxquels ils sont disponibles pour donner des cours. Ces informations sont ensuite utilisées dans la recherche afin de permettre aux élèves de trouver plus facilement un répétiteur disponible au moment souhaité.

## Prérequis

- Python, version 3.13.14 ou une plus récente
- Git
- Le framework Django 
- Un environnement virtuel
- pip
- Pillow (pour les photos de profil)

## Installation des prérequis

### 0. Installation de Python et de pip 

Verifiez que python et pip sont bien intsallés
```bash
python --version
```

Si cette commande ne fonctione pas utilisez 
```bash
python3 --version
```
Si aucune de ces deux commandes ne fonctionne, allez installer python sur [le site officiel python] (https://www.python.org/downloads/)

Puis
```bash
python -m pip --version
```

Et enfin
```bash
git --version
```
Si git n'est pas instellé, allez l'installer depuis [le site officiel](https://git-scm.com/install/?utm_source=chatgpt.com)

### 1. Clonage du code

```bash
git clone https://github.com/oscarharrington22/Travail-de-maturit--code.git
cd Travail-de-maturit--code
cd tutorapp
```

### 2. Création et activation de l'environnement virtuel

Sur macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```
Sur Windows
```bash
python -m venv venv
venv\Scripts\activate
```
Si cela ne fonctionne pas, utilisez :
```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```
Puis ressayez

### 3. Installation des dépendances

```bash
pip install -r requirements.txt
```
ou bien 
```bash
python -m pip install -r requirements.txt
```

### 4. Lancement du site

```bash
python manage.py migrate
python manage.py runserver
```
Le site sera accessibe à :
```bash
http://127.0.0.1:8000/
```


## Outils

- **Python**
- [**Django**](https://docs.djangoproject.com/en/6.0/)
- **HTML**
- [**W3.css**](https://www.w3schools.com/w3css/default.asp)

## Auteur

Application crée par Oscar Harrington dans le cadre du travail de maturité