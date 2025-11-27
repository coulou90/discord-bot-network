class HistoryNode:
    """Un nœud de la liste chaînée."""
    def __init__(self, command: str):
        self.command = command
        self.next = None


class UserHistory:
    """Liste chaînée représentant l'historique des commandes d'un utilisateur."""
    def __init__(self):
        self.head = None   # Premier élément
        self.tail = None   # Dernier élément

    def add_command(self, cmd: str):
        new_node = HistoryNode(cmd)

        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def get_last(self):
        if self.tail:
            return self.tail.command
        return None

    def get_all(self):
        result = []
        current = self.head

        while current:
            result.append(current.command)
            current = current.next

        return result

    def clear(self):
        self.head = None
        self.tail = None