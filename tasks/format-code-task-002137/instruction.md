Les routes pour appeler Hydra depuis udata ont changé pour être davantage RESTful.

Il faut donc changer les appels suivants dans udata :

- Création d'une resource: `POST` vers `[hydra-url]/api/resource/created/` -> doit être changé en `POST` vers `[hydra-url]/api/resources/`. Le payload ne change pas.
- Update d'une resource: `POST` vers `[hydra-url]/api/resource/updated/` -> doit être changé en `PUT` vers `[hydra-url]/api/resources/`. Le payload ne change pas.
- Update d'une resource: `POST` vers `[hydra-url]/api/resource/deleted/` -> doit être changé en `DELETE` vers `[hydra-url]/api/resources/`. Le payload ne change pas.

Les précédentes routes restent fonctionnelles pour l'instant côté hydra pour ne pas créer de breaking change, mais elles sont legacy.

Dès que les routes ont été changées en prod sur uadata, il faudra penser à créer une PR côté hydra pour effacer les routes legacy.

@maudetes @magopian hésitez pas à réattribuer le ticket à qui de droit, y compris moi, si besoin :)
