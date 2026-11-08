# Atelier Paname — site web

Site vitrine et boutique de l'Atelier Paname (Robin Mielleux, Compagnon du Devoir) : ferronnerie d'art, ébénisterie et mobilier sur mesure.

Le site tient dans un seul fichier, `index.html` (HTML, CSS et JavaScript inclus, aucune dépendance à installer).

## Publier avec GitHub Pages

1. Settings → Pages → Source : « Deploy from a branch », branche `main`, dossier `/ (root)`.
2. Le site est servi à `https://gluu-design.github.io/RobinWorkshop/`.
3. Pour un nom de domaine propre, ajouter un fichier `CNAME` contenant le domaine et pointer le DNS vers GitHub Pages.

## Modifier le contenu

Tout le contenu éditable est en tête du `<script>` dans `index.html` :

- `PIECES` : les créations de la galerie (titre, matières, description, dimensions, lieu, année).
- `PRODUCTS` : les articles de la boutique (prix TTC, délai en semaines, dimensions).
- `T` : tous les textes du site en français (`fr`) et en anglais (`en`).
- Coordonnées (adresse, e-mail, téléphone, Instagram, SIRET) : dans le `<footer>` et dans la constante `mail` de la fonction `showDone`.

Pour afficher de vraies photos, renseigner le champ `photo` d'une pièce ou d'un produit avec l'URL de l'image (par exemple `photo:'images/table-enclume.jpg'`) ; la photo remplace alors l'aplat de matière.

## Commandes

Pas de paiement en ligne : la commande génère un récapitulatif que le client copie ou envoie par e-mail à l'atelier (acompte de 30 % à la commande). Un lien de paiement Stripe ou un bouton Shopify peut être branché sur les boutons « Ajouter » ultérieurement.
