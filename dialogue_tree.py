# dialogue_tree.py

class TreeNode:
    def __init__(self, node_id: str, text: str, left=None, right=None, is_leaf=False, result=None):
        self.node_id = node_id
        self.text = text
        self.left = left
        self.right = right
        self.is_leaf = is_leaf
        self.result = result


def build_network_admin_tree():
    # FEUILLES (résultats finaux)
    leaf_cisco_lan = TreeNode(
        "leaf_cisco_lan",
        "",
        is_leaf=True,
        result="🎯 Tu es Administrateur Réseau Cisco (LAN/VLAN)."
    )

    leaf_cisco_sec = TreeNode(
        "leaf_cisco_sec",
        "",
        is_leaf=True,
        result="🔥 Tu es Administrateur Sécurité Réseau (Cisco/FortiGate)."
    )

    leaf_cisco_support = TreeNode(
        "leaf_cisco_support",
        "",
        is_leaf=True,
        result="🔍 Tu es Technicien Support Réseau (N2)."
    )

    leaf_cisco_noc = TreeNode(
        "leaf_cisco_noc",
        "",
        is_leaf=True,
        result="⚡ Tu es Ingénieur Réseau Opérationnel (NOC)."
    )

    leaf_linux_admin = TreeNode(
        "leaf_linux_admin",
        "",
        is_leaf=True,
        result="🧰 Tu es Administrateur Systèmes & Réseau Linux."
    )

    leaf_infra_virtual = TreeNode(
        "leaf_infra_virtual",
        "",
        is_leaf=True,
        result="🖥️ Tu es Ingénieur Infrastructure & Virtualisation (VMs / LXC / Docker…)."
    )

    leaf_devops = TreeNode(
        "leaf_devops",
        "",
        is_leaf=True,
        result="🤖 Tu es DevOps orienté Réseau (automatisation)."
    )

    leaf_monitoring = TreeNode(
        "leaf_monitoring",
        "",
        is_leaf=True,
        result="📈 Tu es Ingénieur Supervision & Monitoring Réseau."
    )

    # NIVEAU 3
    q3_cisco_config = TreeNode(
        "q3_cisco_config",
        "Tu préfères travailler sur :\n"
        "1️⃣ Le réseau interne (LAN, VLAN, WiFi, routage…)\n"
        "2️⃣ La sécurité réseau (pare-feu, VPN, FortiGate, ACL…) ",
        left=leaf_cisco_lan,
        right=leaf_cisco_sec
    )

    q3_cisco_depannage = TreeNode(
        "q3_cisco_depannage",
        "En dépannage réseau, tu te vois plutôt :\n"
        "1️⃣ En analyse (Wireshark, logs, pings…)\n"
        "2️⃣ En intervention rapide (NOC, incidents…)",
        left=leaf_cisco_support,
        right=leaf_cisco_noc
    )

    q3_linux_services = TreeNode(
        "q3_linux_services",
        "Tu préfères gérer :\n"
        "1️⃣ Des serveurs critiques (DNS, DHCP, web, VPN…)\n"
        "2️⃣ Des environnements virtualisés (VMs / LXC / Docker…)",
        left=leaf_linux_admin,
        right=leaf_infra_virtual
    )

    q3_linux_auto = TreeNode(
        "q3_linux_auto",
        "Tu veux automatiser :\n"
        "1️⃣ Les déploiements / configs (Ansible, scripts…)\n"
        "2️⃣ La supervision (Prometheus, Grafana…)",
        left=leaf_devops,
        right=leaf_monitoring
    )

    # NIVEAU 2
    q2_cisco = TreeNode(
        "q2_cisco",
        "Avec Cisco, tu préfères :\n"
        "1️⃣ La configuration (VLAN, WiFi, DHCP, routage…)\n"
        "2️⃣ Le dépannage (incidents, analyse…)",
        left=q3_cisco_config,
        right=q3_cisco_depannage
    )

    q2_linux = TreeNode(
        "q2_linux",
        "Sur Linux, tu préfères travailler sur :\n"
        "1️⃣ L'administration réseau (DNS, DHCP, web…)\n"
        "2️⃣ L'automatisation / scripts",
        left=q3_linux_services,
        right=q3_linux_auto
    )

    # RACINE
    root = TreeNode(
        "root",
        "Tu préfères travailler surtout avec :\n"
        "1️⃣ Des équipements réseau Cisco\n"
        "2️⃣ Des serveurs et systèmes Linux",
        left=q2_cisco,
        right=q2_linux
    )

    return root


def search_topic(node: TreeNode, topic: str) -> bool:
    """Recherche d’un mot-clé dans tout l’arbre."""
    if node is None:
        return False

    text = (node.text or "") + " " + (node.result or "")
    if topic.lower() in text.lower():
        return True

    return search_topic(node.left, topic) or search_topic(node.right, topic)