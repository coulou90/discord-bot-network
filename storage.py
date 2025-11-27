import json
from history import UserHistory, HistoryNode

SAVE_FILE = "data/save.json"


def save_data(histories, user_positions, xp):
    data = {
        "histories": {},
        "positions": {},
        "xp": xp
    }

    # Sauvegarde des historiques
    for user_id, history in histories.items():
        commands_list = history.get_all()
        data["histories"][str(user_id)] = commands_list

    # Sauvegarde de la position dans l'arbre
    for user_id, node in user_positions.items():
        data["positions"][str(user_id)] = node.node_id

    # Écriture fichier JSON
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print("✔ Données sauvegardées.")


def load_data(tree_root, histories, user_positions, xp):
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Aucune sauvegarde trouvée.")
        return

    # --- Charger les historiques ---
    for user_id, cmd_list in data.get("histories", {}).items():
        uh = UserHistory()
        for cmd in cmd_list:
            uh.add_command(cmd)
        histories[int(user_id)] = uh

    # --- Recherche d'un noeud par ID ---
    def find_node(root, node_id):
        if root.node_id == node_id:
            return root
        if root.left:
            left = find_node(root.left, node_id)
            if left:
                return left
        if root.right:
            return find_node(root.right, node_id)
        return None

    # --- Charger les positions ---
    for user_id, node_id in data.get("positions", {}).items():
        node = find_node(tree_root, node_id)
        if node:
            user_positions[int(user_id)] = node

    # --- Charger XP ---
    stored_xp = data.get("xp", {})
    xp.update(stored_xp)

    print("✔ Données chargées.")