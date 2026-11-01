# nutrition_insuline : qualité des données NHANES avec dbt

Projet personnel de **qualité et de documentation des données** (dbt Core + BigQuery) sur les données publiques NHANES (CDC), cycle août 2021 - août 2023 : insuline et glycémie à jeun, mesures corporelles, activité physique déclarée.

> **Ce projet ne contient aucune analyse médicale, aucune conclusion clinique et aucun conseil de santé.** C'est un projet de qualité de données.

## Problématique

Peut-on calculer un indice HOMA-IR fiable à partir de NHANES ? Quelles règles de qualité faut-il appliquer, et combien de participants écartent-elles ?

## Pipeline

```
fichiers .xpt (CDC) -> BigQuery nhanes_raw -> staging (6 vues) -> mart_participants (1 table)
```

![Lignage dbt](docs/lineage.png)

| Couche | Contenu |
|---|---|
| `nhanes_raw` | 6 fichiers chargés tels quels (démographie, mesures corporelles, insuline, glycémie, activité physique, questionnaire de jeûne) |
| `staging` | Renommage, typage, recodage des valeurs spéciales, une vue par table |
| `marts` | `mart_participants` : un participant examiné par ligne, HOMA-IR et motif d'exclusion |

## Règles de qualité appliquées

- **Valeurs "refus" et "ne sait pas"** recodées en vide (éducation : 7 et 9 ; activité physique : 7777 et 9999), avec un indicateur booléen pour garder la trace.
- **Zéros mal lus** : après lecture des fichiers XPT avec pandas, des valeurs de l'ordre de 5e-79 apparaissaient à la place de 0 (heures et minutes de jeûne, code de limite de détection). La macro `clean_zero` les corrige en staging ; la table brute reste intacte. Un test dbt vérifie qu'il n'en reste aucun.
- **Critère de jeûne officiel du CDC** : 8 heures à moins de 24 heures. Les autres participants sont exclus du calcul.
- **Adultes uniquement** (18 ans et plus), aligné sur le questionnaire d'activité physique.
- **Grossesse** : les femmes enceintes et les cas indéterminés sont exclus.
- **Plausibilité** : bornes volontairement larges sur poids, taille, IMC et tour de taille, et cohérence de l'IMC avec le poids et la taille.
- **Cohérence fréquence / unité** (activité physique) : une fréquence positive a toujours une unité, une fréquence nulle n'en a jamais.
- **Tests dbt** sur les clés (unicité, non-nullité), les liens entre tables (`relationships`), les valeurs autorisées (`accepted_values`) et des tests de cohérence écrits sur mesure. Tous passent.

## Résultat de la sélection

8 860 participants ont été examinés (sur 11 933 dans le fichier de démographie). Chacun est classé par le **premier** motif d'exclusion rencontré :

| Motif | Participants |
|---|---|
| Insuline ou glycémie manquante | 3 179 |
| Moins de 18 ans | 2 523 |
| Jeûne hors 8 h à moins de 24 h | 238 |
| Grossesse ou statut indéterminé | 36 |
| Durée de jeûne inconnue | 2 |
| **Retenus pour le HOMA-IR** | **2 882** |

Les motifs sont exclusifs et appliqués dans cet ordre : un participant n'est compté que dans le premier qui le concerne.

## HOMA-IR

`glycémie à jeun (mg/dL) x insuline à jeun (uU/mL) / 405`, soit l'approximation courante de la formule d'origine (glycémie en mmol/L x insuline / 22,5), avec la glycémie convertie en mg/dL. Le CDC ne fournit pas de formule dans la documentation du fichier insuline.

## Limites

- Les chiffres décrivent **cet échantillon**, pas la population américaine : les poids de sondage sont conservés dans la table mais ne sont pas utilisés.
- Les participants hors critère de jeûne officiel mais avec une insuline mesurée ne sont pas repondérés.
- Le cycle 2021-2023 est le plus récent publié ; le cycle 2025-2027 est en cours de collecte.
- Les seuils de plausibilité sont des choix du projet, pas des normes.
- L'approximation du HOMA-IR utilisée ici date de 1985 et n'est pas recalibrée pour les dosages d'insuline actuels (une version HOMA2 existe).
- Les analyses descriptives (association activité physique / HOMA-IR) ne sont pas encore écrites.

## Reproduire

1. Compte Google Cloud, projet avec BigQuery, `gcloud auth application-default login`.
2. `pip install dbt-bigquery pandas pyarrow` (Python 3.11).
3. Télécharger depuis le CDC (suffixe `_L`, cycle 2021-2023) : `DEMO_L`, `BMX_L`, `INS_L`, `GLU_L`, `PAQ_L`, `FASTQX_L`, dans `data/raw/`.
4. Adapter `PROJECT` dans `scripts/load_nhanes.py`, puis `python scripts/load_nhanes.py`.
5. Copier `profiles.yml.example` en `profiles.yml` (en mettant votre projet GCP).
6. `export DBT_PROFILES_DIR=. && dbt run && dbt test`.
7. `dbt docs generate && dbt docs serve`.

## Source des données

NHANES, National Center for Health Statistics, CDC. Données publiques.

## Références

- Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. Homeostasis model assessment: insulin resistance and β-cell function from fasting plasma glucose and insulin concentrations in man. Diabetologia. 1985;28(7):412-419. https://doi.org/10.1007/BF00280883