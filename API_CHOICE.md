# API Choice

# API Choice

- Étudiant : UlrichVianney
- API choisie : Agify
- URL base : https://api.agify.io
- Documentation officielle / README : https://agify.io
- Auth : None
- Endpoints testés :
  - GET /?name={name}
  - GET /?name= (entrée invalide)
- Hypothèses de contrat (champs attendus, types, codes) :
  - Champs : name (string), age (int|null), count (int)
  - Code HTTP : 200 pour requête valide
  - Content-Type : application/json
- Limites / rate limiting connu : 100 requêtes/jour sans clé
- Risques : rate limit bas sans clé API