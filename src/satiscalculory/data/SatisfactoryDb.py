"""
SatisfactoryData.py
"""
import sqlite3
from sqlite3 import Connection, Cursor
import os.path

from .SatisfactoryWikiPage import SatisfactoryWikiPage


class SatisfactoryDb:
    # I did this in a sort of unorthodox way with Excel. I've uploaded the Excel file to /util/other/ for edification.
    item_links: dict[str:str] = {
        "Adaptive Control Unit": "https://satisfactory.wiki.gg/wiki/Adaptive_Control_Unit",
        "AI Expansion Server": "https://satisfactory.wiki.gg/wiki/AI_Expansion_Server",
        "AI Limiter": "https://satisfactory.wiki.gg/wiki/AI_Limiter",
        "Alclad Aluminum Sheet": "https://satisfactory.wiki.gg/wiki/Alclad_Aluminum_Sheet",
        "Alien DNA Capsule": "https://satisfactory.wiki.gg/wiki/Alien_DNA_Capsule",
        "Alien Power Matrix": "https://satisfactory.wiki.gg/wiki/Alien_Power_Matrix",
        "Alien Protein": "https://satisfactory.wiki.gg/wiki/Alien_Protein",
        "Alien Remains": "https://satisfactory.wiki.gg/wiki/Alien_Remains",
        "Aluminum Casing": "https://satisfactory.wiki.gg/wiki/Aluminum_Casing",
        "Aluminum Ingot": "https://satisfactory.wiki.gg/wiki/Aluminum_Ingot",
        "Aluminum Scrap": "https://satisfactory.wiki.gg/wiki/Aluminum_Scrap",
        "Assembly Director System": "https://satisfactory.wiki.gg/wiki/Assembly_Director_System",
        "Automated Wiring": "https://satisfactory.wiki.gg/wiki/Automated_Wiring",
        "Bacon Agaric": "https://satisfactory.wiki.gg/wiki/Bacon_Agaric",
        "Ballistic Warp Drive": "https://satisfactory.wiki.gg/wiki/Ballistic_Warp_Drive",
        "Battery": "https://satisfactory.wiki.gg/wiki/Battery",
        "Bauxite": "https://satisfactory.wiki.gg/wiki/Bauxite",
        "Beacon": "https://satisfactory.wiki.gg/wiki/Beacon",
        "Beryl Nut": "https://satisfactory.wiki.gg/wiki/Beryl_Nut",
        "Biochemical Sculptor": "https://satisfactory.wiki.gg/wiki/Biochemical_Sculptor",
        "Biomass": "https://satisfactory.wiki.gg/wiki/Biomass",
        "Black Powder": "https://satisfactory.wiki.gg/wiki/Black_Powder",
        "Blade Runners": "https://satisfactory.wiki.gg/wiki/Blade_Runners",
        "Boom Box": "https://satisfactory.wiki.gg/wiki/Boom_Box",
        "Cable": "https://satisfactory.wiki.gg/wiki/Cable",
        "Caterium Ingot": "https://satisfactory.wiki.gg/wiki/Caterium_Ingot",
        "Caterium Ore": "https://satisfactory.wiki.gg/wiki/Caterium_Ore",
        "Chainsaw": "https://satisfactory.wiki.gg/wiki/Chainsaw",
        "Circuit Board": "https://satisfactory.wiki.gg/wiki/Circuit_Board",
        "Coal": "https://satisfactory.wiki.gg/wiki/Coal",
        "Color Cartridge": "https://satisfactory.wiki.gg/wiki/Color_Cartridge",
        "Compacted Coal": "https://satisfactory.wiki.gg/wiki/Compacted_Coal",
        "Computer": "https://satisfactory.wiki.gg/wiki/Computer",
        "Concrete": "https://satisfactory.wiki.gg/wiki/Concrete",
        "Cooling System": "https://satisfactory.wiki.gg/wiki/Cooling_System",
        "Copper Ingot": "https://satisfactory.wiki.gg/wiki/Copper_Ingot",
        "Copper Ore": "https://satisfactory.wiki.gg/wiki/Copper_Ore",
        "Copper Powder": "https://satisfactory.wiki.gg/wiki/Copper_Powder",
        "Copper Sheet": "https://satisfactory.wiki.gg/wiki/Copper_Sheet",
        "Crude Oil": "https://satisfactory.wiki.gg/wiki/Crude_Oil",
        "Crystal Oscillator": "https://satisfactory.wiki.gg/wiki/Crystal_Oscillator",
        "Cup": "https://satisfactory.wiki.gg/wiki/Cup",
        "Dark Matter Crystal": "https://satisfactory.wiki.gg/wiki/Dark_Matter_Crystal",
        "Diamonds": "https://satisfactory.wiki.gg/wiki/Diamonds",
        "Electromagnetic Control Rod": "https://satisfactory.wiki.gg/wiki/Electromagnetic_Control_Rod",
        "Empty Canister": "https://satisfactory.wiki.gg/wiki/Empty_Canister",
        "Empty Fluid Tank": "https://satisfactory.wiki.gg/wiki/Empty_Fluid_Tank",
        "Encased Industrial Beam": "https://satisfactory.wiki.gg/wiki/Encased_Industrial_Beam",
        "Encased Plutonium Cell": "https://satisfactory.wiki.gg/wiki/Encased_Plutonium_Cell",
        "Encased Uranium Cell": "https://satisfactory.wiki.gg/wiki/Encased_Uranium_Cell",
        "Fabric": "https://satisfactory.wiki.gg/wiki/Fabric",
        "FICSIT Coupon": "https://satisfactory.wiki.gg/wiki/FICSIT_Coupon",
        "Ficsite Ingot": "https://satisfactory.wiki.gg/wiki/Ficsite_Ingot",
        "Ficsite Trigon": "https://satisfactory.wiki.gg/wiki/Ficsite_Trigon",
        "FICSMAS/Equipment": "https://satisfactory.wiki.gg/wiki/FICSMAS/Equipment",
        "Ficsonium": "https://satisfactory.wiki.gg/wiki/Ficsonium",
        "Ficsonium Fuel Rod": "https://satisfactory.wiki.gg/wiki/Ficsonium_Fuel_Rod",
        "Flower Petals": "https://satisfactory.wiki.gg/wiki/Flower_Petals",
        "Fused Modular Frame": "https://satisfactory.wiki.gg/wiki/Fused_Modular_Frame",
        "Gas Mask": "https://satisfactory.wiki.gg/wiki/Gas_Mask",
        "Hard Drive": "https://satisfactory.wiki.gg/wiki/Hard_Drive",
        "Hazmat Suit": "https://satisfactory.wiki.gg/wiki/Hazmat_Suit",
        "Heat Sink": "https://satisfactory.wiki.gg/wiki/Heat_Sink",
        "Heavy Modular Frame": "https://satisfactory.wiki.gg/wiki/Heavy_Modular_Frame",
        "High-Speed Connector": "https://satisfactory.wiki.gg/wiki/High-Speed_Connector",
        "Hoverpack": "https://satisfactory.wiki.gg/wiki/Hoverpack",
        "HUB Parts": "https://satisfactory.wiki.gg/wiki/HUB_Parts",
        "Iron Ingot": "https://satisfactory.wiki.gg/wiki/Iron_Ingot",
        "Iron Ore": "https://satisfactory.wiki.gg/wiki/Iron_Ore",
        "Iron Plate": "https://satisfactory.wiki.gg/wiki/Iron_Plate",
        "Iron Rod": "https://satisfactory.wiki.gg/wiki/Iron_Rod",
        "Jetpack": "https://satisfactory.wiki.gg/wiki/Jetpack",
        "Leaves": "https://satisfactory.wiki.gg/wiki/Leaves",
        "Limestone": "https://satisfactory.wiki.gg/wiki/Limestone",
        "Magnetic Field Generator": "https://satisfactory.wiki.gg/wiki/Magnetic_Field_Generator",
        "Medicinal Inhaler": "https://satisfactory.wiki.gg/wiki/Medicinal_Inhaler",
        "Mercer Sphere": "https://satisfactory.wiki.gg/wiki/Mercer_Sphere",
        "Miner": "https://satisfactory.wiki.gg/wiki/Miner",
        "Modular Engine": "https://satisfactory.wiki.gg/wiki/Modular_Engine",
        "Modular Frame": "https://satisfactory.wiki.gg/wiki/Modular_Frame",
        "Motor": "https://satisfactory.wiki.gg/wiki/Motor",
        "Mycelia": "https://satisfactory.wiki.gg/wiki/Mycelia",
        "Neural-Quantum Processor": "https://satisfactory.wiki.gg/wiki/Neural-Quantum_Processor",
        "Nobelisk Detonator": "https://satisfactory.wiki.gg/wiki/Nobelisk_Detonator",
        "Non-Fissile Uranium": "https://satisfactory.wiki.gg/wiki/Non-Fissile_Uranium",
        "Nuclear Pasta": "https://satisfactory.wiki.gg/wiki/Nuclear_Pasta",
        "Object Scanner": "https://satisfactory.wiki.gg/wiki/Object_Scanner",
        "User:Ondar111/sandbox": "https://satisfactory.wiki.gg/wiki/User:Ondar111/sandbox",
        "Packaged Alumina Solution": "https://satisfactory.wiki.gg/wiki/Packaged_Alumina_Solution",
        "Packaged Fuel": "https://satisfactory.wiki.gg/wiki/Packaged_Fuel",
        "Packaged Heavy Oil Residue": "https://satisfactory.wiki.gg/wiki/Packaged_Heavy_Oil_Residue",
        "Packaged Ionized Fuel": "https://satisfactory.wiki.gg/wiki/Packaged_Ionized_Fuel",
        "Packaged Liquid Biofuel": "https://satisfactory.wiki.gg/wiki/Packaged_Liquid_Biofuel",
        "Packaged Nitric Acid": "https://satisfactory.wiki.gg/wiki/Packaged_Nitric_Acid",
        "Packaged Nitrogen Gas": "https://satisfactory.wiki.gg/wiki/Packaged_Nitrogen_Gas",
        "Packaged Oil": "https://satisfactory.wiki.gg/wiki/Packaged_Oil",
        "Packaged Rocket Fuel": "https://satisfactory.wiki.gg/wiki/Packaged_Rocket_Fuel",
        "Packaged Sulfuric Acid": "https://satisfactory.wiki.gg/wiki/Packaged_Sulfuric_Acid",
        "Packaged Turbofuel": "https://satisfactory.wiki.gg/wiki/Packaged_Turbofuel",
        "Packaged Water": "https://satisfactory.wiki.gg/wiki/Packaged_Water",
        "Paleberry": "https://satisfactory.wiki.gg/wiki/Paleberry",
        "Parachute": "https://satisfactory.wiki.gg/wiki/Parachute",
        "Petroleum Coke": "https://satisfactory.wiki.gg/wiki/Petroleum_Coke",
        "Plastic": "https://satisfactory.wiki.gg/wiki/Plastic",
        "Plutonium Fuel Rod": "https://satisfactory.wiki.gg/wiki/Plutonium_Fuel_Rod",
        "Plutonium Pellet": "https://satisfactory.wiki.gg/wiki/Plutonium_Pellet",
        "Plutonium Waste": "https://satisfactory.wiki.gg/wiki/Plutonium_Waste",
        "Polymer Resin": "https://satisfactory.wiki.gg/wiki/Polymer_Resin",
        "Power Shard": "https://satisfactory.wiki.gg/wiki/Power_Shard",
        "Power Slug": "https://satisfactory.wiki.gg/wiki/Power_Slug",
        "Pressure Conversion Cube": "https://satisfactory.wiki.gg/wiki/Pressure_Conversion_Cube",
        "Quartz Crystal": "https://satisfactory.wiki.gg/wiki/Quartz_Crystal",
        "Quickwire": "https://satisfactory.wiki.gg/wiki/Quickwire",
        "Radio Control Unit": "https://satisfactory.wiki.gg/wiki/Radio_Control_Unit",
        "Raw Quartz": "https://satisfactory.wiki.gg/wiki/Raw_Quartz",
        "Reanimated SAM": "https://satisfactory.wiki.gg/wiki/Reanimated_SAM",
        "Rebar Gun": "https://satisfactory.wiki.gg/wiki/Rebar_Gun",
        "Reinforced Iron Plate": "https://satisfactory.wiki.gg/wiki/Reinforced_Iron_Plate",
        "Rifle": "https://satisfactory.wiki.gg/wiki/Rifle",
        "Rotor": "https://satisfactory.wiki.gg/wiki/Rotor",
        "Rubber": "https://satisfactory.wiki.gg/wiki/Rubber",
        "SAM": "https://satisfactory.wiki.gg/wiki/SAM",
        "SAM Fluctuator": "https://satisfactory.wiki.gg/wiki/SAM_Fluctuator",
        "Screw": "https://satisfactory.wiki.gg/wiki/Screw",
        "Silica": "https://satisfactory.wiki.gg/wiki/Silica",
        "Singularity Cell": "https://satisfactory.wiki.gg/wiki/Singularity_Cell",
        "Smart Plating": "https://satisfactory.wiki.gg/wiki/Smart_Plating",
        "Smokeless Powder": "https://satisfactory.wiki.gg/wiki/Smokeless_Powder",
        "Solid Biofuel": "https://satisfactory.wiki.gg/wiki/Solid_Biofuel",
        "Somersloop": "https://satisfactory.wiki.gg/wiki/Somersloop",
        "Somersloop/zh": "https://satisfactory.wiki.gg/wiki/Somersloop/zh",
        "Stator": "https://satisfactory.wiki.gg/wiki/Stator",
        "Statues": "https://satisfactory.wiki.gg/wiki/Statues",
        "Steel Beam": "https://satisfactory.wiki.gg/wiki/Steel_Beam",
        "Steel Ingot": "https://satisfactory.wiki.gg/wiki/Steel_Ingot",
        "Steel Pipe": "https://satisfactory.wiki.gg/wiki/Steel_Pipe",
        "Sulfur": "https://satisfactory.wiki.gg/wiki/Sulfur",
        "Supercomputer": "https://satisfactory.wiki.gg/wiki/Supercomputer",
        "Superposition Oscillator": "https://satisfactory.wiki.gg/wiki/Superposition_Oscillator",
        "Thermal Propulsion Rocket": "https://satisfactory.wiki.gg/wiki/Thermal_Propulsion_Rocket",
        "Time Crystal": "https://satisfactory.wiki.gg/wiki/Time_Crystal",
        "Turbo Motor": "https://satisfactory.wiki.gg/wiki/Turbo_Motor",
        "Uranium": "https://satisfactory.wiki.gg/wiki/Uranium",
        "Uranium Fuel Rod": "https://satisfactory.wiki.gg/wiki/Uranium_Fuel_Rod",
        "Uranium Waste": "https://satisfactory.wiki.gg/wiki/Uranium_Waste",
        "Versatile Framework": "https://satisfactory.wiki.gg/wiki/Versatile_Framework",
        "Vines": "https://satisfactory.wiki.gg/wiki/Vines",
        "Wire": "https://satisfactory.wiki.gg/wiki/Wire",
        "Wood": "https://satisfactory.wiki.gg/wiki/Wood",
        "Xeno-Basher": "https://satisfactory.wiki.gg/wiki/Xeno-Basher",
        "Xeno-Zapper": "https://satisfactory.wiki.gg/wiki/Xeno-Zapper",
        "Zipline": "https://satisfactory.wiki.gg/wiki/Zipline",
    }

    def __init__(self) -> None:
        print("Fetching item and recipe data from https://satisfactory.wiki.gg/...")
        with sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), "satisfactory_items.sqlite")) as connection:
            print("Connected to local SQLite database successfully!")
            print("Clearing existing data.")

            cursor: Cursor = connection.cursor()

            # Drop existing tables.
            cursor.execute("DROP TABLE items;")
            cursor.execute("DROP TABLE recipes;")

            # Create new tables.
            cursor.execute(
                "CREATE TABLE items ("
                "name TEXT PRIMARY KEY,"
                "stack_size INTEGER,"
                "sink_points INTEGER"
                ");"
            )

            cursor.execute(
                "CREATE TABLE recipes ("
                "name TEXT PRIMARY KEY,"
                "ingredients TEXT,"
                "ingredient_rates REAL,"
                "facility TEXT,"
                "facility_rates REAL,"
                "products TEXT,"
                "product_rates REAL,"
                "item TEXT,"
                "FOREIGN KEY (item) REFERENCES items(name)"
                ");"
            )

            for item_name, link in self.item_links.items():
                print(f"Fetching data for {item_name} from {link}.")
                page: SatisfactoryWikiPage = SatisfactoryWikiPage(link)

                # Inserts the new data into the table.
                cursor.execute(
                    "INSERT INTO items (name, stack_size, sink_points)"
                    "VALUES (?, ?, ?)",
                    (page.item.name, page.item.stack_size, page.item.sink_points)
                )

                for recipe in page.item.recipes:
                    ingredient_names: str = ""
                    ingredient_rates: str = ""
                    product_names: str = ""
                    product_rates: str = ""

                    for name, rate in recipe.ingredients:
                        ingredient_names += f"{name}, "
                        ingredient_rates += f"{rate}, "

                    else:
                        ingredient_names = ingredient_names[:-2]
                        ingredient_rates = ingredient_rates[:-2]

                    for name, rate in recipe.products:
                        product_names += f"{name}, "
                        product_rates += f"{rate}, "

                    else:
                        product_names.removesuffix(", ")
                        product_rates.removesuffix(", ")

                    cursor.execute(
                        "INSERT INTO recipes (name, ingredients, ingredient_rates, facility, facility_rates, products, product_rates, item)"
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (recipe.name, ingredient_names, ingredient_rates, recipe.facility[0], recipe.facility[1], product_names, product_rates, page.item.name)
                    )

            connection.commit()
            connection.close()

if __name__ == "__main__":
    main: SatisfactoryDb = SatisfactoryDb()
