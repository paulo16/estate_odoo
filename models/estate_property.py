from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    """
    Modèle principal pour gérer les propriétés immobilières
    
    Ce modèle représente une propriété immobilière avec toutes ses caractéristiques :
    - Informations de base (nom, description, prix)
    - Caractéristiques physiques (surface, chambres, jardin)  
    - Informations de vente (prix attendu, prix de vente, état)
    - Données de disponibilité et localisation
    """
    
    # ========================================
    # DÉFINITION DU MODÈLE
    # ========================================
    _name = "estate.property"                    # 🆔 Nom technique unique du modèle
    _description = "Real Estate Property"        # 📝 Description pour les développeurs
    _order = "id desc"                          # 📊 Tri par défaut (plus récent en premier)
    _rec_name = "name"                          # 🏷️ Champ utilisé pour l'affichage des records
    
    # ========================================
    # CHAMPS DE BASE
    # ========================================
    
    # 📝 Informations générales
    name = fields.Char(
        string='Title',                          # 🏷️ Libellé affiché à l'utilisateur
        required=True,                          # ⭐ Champ obligatoire
        help="Enter the property title"        # ❓ Aide contextuelle
    )
    
    description = fields.Text(
        string='Description',
        help="Detailed description of the property"
    )
    
    # 📍 Localisation
    postcode = fields.Char(
        string='Postcode',
        size=10,                                # 📏 Limite de caractères
        help="Postal code of the property location"
    )
    
    # 📅 Dates importantes  
    date_availability = fields.Date(
        string='Available From',
        copy=False,                             # 🚫 Ne pas copier lors de la duplication
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        help="Date when the property becomes available"
    )
    
    # 💰 Informations financières
    expected_price = fields.Float(
        string='Expected Price',
        required=True,                          # ⭐ Obligatoire
        help="Expected selling price in company currency"
    )
    
    selling_price = fields.Float(
        string='Selling Price',
        readonly=True,                          # 🔒 Lecture seule (sera rempli automatiquement)
        copy=False,                            # 🚫 Ne pas copier lors de la duplication
        help="Final selling price (filled automatically when offer accepted)"
    )
    
    # 🏠 Caractéristiques physiques
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2,                              # 🎯 Valeur par défaut
        help="Number of bedrooms"
    )
    
    living_area = fields.Integer(
        string='Living Area (sqm)',
        help="Living area in square meters"
    )
    
    facades = fields.Integer(
        string='Facades',
        help="Number of facades"
    )
    
    # 🅱️ Options booléennes
    garage = fields.Boolean(
        string='Garage',
        help="Does the property have a garage?"
    )
    
    garden = fields.Boolean(
        string='Garden',
        help="Does the property have a garden?"
    )
    
    # 🌳 Spécificités jardin
    garden_area = fields.Integer(
        string='Garden Area (sqm)',
        help="Garden area in square meters"
    )
    
    garden_orientation = fields.Selection(
        selection=[                             # 📋 Liste de choix prédéfinis
            ('north', 'North'),                # (valeur_stockée, 'Libellé affiché')
            ('south', 'South'), 
            ('east', 'East'),
            ('west', 'West'),
        ],
        string='Garden Orientation',
        help="Orientation of the garden"
    )
    
    # ========================================
    # CHAMPS SYSTÈME ET ÉTAT
    # ========================================
    
    active = fields.Boolean(
        string='Active',
        default=True,                           # 🎯 Actif par défaut
        help="Uncheck to archive the property (won't be visible in normal views)"
    )
    
    state = fields.Selection(
        selection=[
            ('new', 'New'),                    # 🆕 Nouveau (état initial)
            ('offer_received', 'Offer Received'), # 💌 Offre reçue
            ('offer_accepted', 'Offer Accepted'), # ✅ Offre acceptée
            ('sold', 'Sold'),                  # 💰 Vendu
            ('cancelled', 'Cancelled'),        # ❌ Annulé
        ],
        string='Status',
        required=True,                          # ⭐ Obligatoire
        copy=False,                            # 🚫 Ne pas copier
        default='new',                         # 🎯 État initial = "new"
        help="Status of the property in the sales process"
    )

    # ========================================
    # MÉTHODES SPÉCIALES (seront étendues dans les chapitres suivants)
    # ========================================
    
    def name_get(self):
        """
        Personnalise l'affichage du nom du record dans les listes déroulantes
        
        Au lieu d'afficher juste le titre, on peut afficher "Titre - Code Postal"
        """
        result = []
        for record in self:
            name = record.name
            if record.postcode:
                name = f"{name} - {record.postcode}"
            result.append((record.id, name))
        return result
    
    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """
        Personnalise la recherche dans les champs Many2one
        
        Permet de rechercher par nom OU par code postal
        """
        args = args or []
        if name:
            args = ['|', ('name', operator, name), ('postcode', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)