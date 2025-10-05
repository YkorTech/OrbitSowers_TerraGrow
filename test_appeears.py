"""
Script de test AppEEARS API
Teste l'extraction de données NDVI pour Yaoundé
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.appeears_api import AppEEARSAPI


def test_appeears():
    """Test AppEEARS API"""

    print("=" * 60)
    print("🧪 TEST AppEEARS API - TerraGrow")
    print("=" * 60)

    # Initialize API
    api = AppEEARSAPI()

    # --- ÉTAPE 1 : LOGIN ---
    print("\n📝 ÉTAPE 1/5 : Login NASA Earthdata")
    print("-" * 60)

    # TODO: Remplacer par vos vrais identifiants
    username = input("Entrez votre username NASA Earthdata: ")
    password = input("Entrez votre password NASA Earthdata: ")

    if not api.login(username, password):
        print("❌ Login échoué. Vérifiez vos identifiants.")
        return

    # --- ÉTAPE 2 : SEARCH PRODUCTS (optionnel) ---
    print("\n🔍 ÉTAPE 2/5 : Recherche produits disponibles")
    print("-" * 60)

    print("\nRecherche NDVI products...")
    ndvi_products = api.search_products("NDVI")

    print(f"\n✅ Trouvé {len(ndvi_products)} produits NDVI:")
    for i, product in enumerate(ndvi_products[:5]):  # Show first 5
        print(f"   {i+1}. {product['ProductAndVersion']} - {product['Description']}")
        print(f"      Source: {product['Source']} | Résolution: {product.get('Resolution', 'N/A')}")

    print("\nRecherche SMAP products...")
    smap_products = api.search_products("SMAP")

    print(f"\n✅ Trouvé {len(smap_products)} produits SMAP:")
    for i, product in enumerate(smap_products[:3]):  # Show first 3
        print(f"   {i+1}. {product['ProductAndVersion']} - {product['Description']}")
        print(f"      Source: {product['Source']} | Résolution: {product.get('Resolution', 'N/A')}")

    # --- ÉTAPE 3 : EXTRACT DATA ---
    print("\n📡 ÉTAPE 3/5 : Extraction données pour Yaoundé")
    print("-" * 60)

    print("\nConfiguration:")
    print("   Région: Yaoundé, Cameroun")
    print("   Latitude: 3.87°N")
    print("   Longitude: 11.52°E")
    print("   Produit: MOD13Q1.061 (MODIS NDVI)")
    print("   Période: 12 derniers mois")

    # Extract data
    result = api.extract_ndvi_smap_data(
        lat=3.87,
        lon=11.52,
        region_name="Yaounde_Cameroun",
        output_dir="data/appeears"
    )

    # --- ÉTAPE 4 : RESULTS ---
    print("\n📊 ÉTAPE 4/5 : Résultats")
    print("-" * 60)

    if result:
        print(f"\n✅ Extraction réussie!")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Fichiers téléchargés: {len(result['files'])}")
        print(f"   Fichier CSV: {result['csv_file']}")

        # Show CSV preview
        if os.path.exists(result['csv_file']):
            print(f"\n📄 Aperçu du fichier CSV:")
            with open(result['csv_file'], 'r') as f:
                lines = f.readlines()[:10]  # First 10 lines
                for line in lines:
                    print(f"   {line.strip()}")
    else:
        print("\n❌ Extraction échouée")

    # --- ÉTAPE 5 : NEXT STEPS ---
    print("\n🚀 ÉTAPE 5/5 : Prochaines étapes")
    print("-" * 60)
    print("""
    Si le test a réussi, vous pouvez maintenant:

    1. Examiner le fichier CSV téléchargé dans data/appeears/
    2. Adapter le code pour extraire les 15 régions
    3. Parser les CSV et intégrer au jeu TerraGrow
    4. Remplacer les simulations par les vraies données MODIS
    """)

    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ")
    print("=" * 60)


if __name__ == "__main__":
    test_appeears()
