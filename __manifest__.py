# -*- coding: utf-8 -*-
{
    "name": "Real Estate",  # Titre du module
    "version": "1.0",  # Version du module
    "summary": "Publicité immobilière",  # Résumé du module
    "installable": True,  # Le module peut être installé
    "author": "Paul Mbilong",  # Auteur du module
    "category": "Real Estate",  # Catégorie du module
    "depends": ["base"],  # Dépendances du module
    "application": True,  # Le module est une application
    "data": [
        "security/estate_security.xml",  # 1️⃣ D'abord les groupes
        "security/ir.model.access.csv",  # 2️⃣ Puis les droits d'accès
        "views/estate_property_views.xml",  # 3️⃣ Enfin les vues
    ],
}
