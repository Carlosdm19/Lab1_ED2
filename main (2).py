import pandas as pd
from anytree import Node, RenderTree

class TreeNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None
        self.height = 1

def get_height(node):
    if node is None:
        return 0
    return node.height

def get_balance_factor(node):
    if node is None:
        return 0
    return get_height(node.left) - get_height(node.right)

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if not self.root:
            self.root = TreeNode(key, data)
        else:
            self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if not node:
            return TreeNode(key, data)

        if key < node.key:
            node.left = self._insert(node.left, key, data)
        else:
            node.right = self._insert(node.right, key, data)

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and key < node.left.key:
            return self.rotate_right(node)

        if balance < -1 and key > node.right.key:
            return self.rotate_left(node)

        if balance > 1 and key > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and key < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def rotate_left(self, z):
        if z is None or z.right is None:
            return z

        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(get_height(z.left), get_height(z.right))
        y.height = 1 + max(get_height(y.left), get_height(y.right))

        return y

    def rotate_right(self, y):
        if y is None or y.left is None:
            return y

        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(get_height(y.left), get_height(y.right))
        x.height = 1 + max(get_height(x.left), get_height(x.right))

    def insert_property(self, property_data):
        metric1 = property_data['price'] / property_data['surface_total']
        self.root = self._insert_property(self.root, metric1, property_data)

    def _insert_property(self, node, metric1, property_data):
        if not node:
            return TreeNode(metric1, property_data)

        if metric1 < node.key:
            node.left = self._insert_property(node.left, metric1, property_data)
        elif metric1 > node.key:
            node.right = self._insert_property(node.right, metric1, property_data)
        else:
            metric2 = property_data['price'] / (property_data['surface_total'] + property_data['bedrooms'] + property_data['bathrooms'])
            node.right = self._insert_property(node.right, metric1, property_data)  # Insertar en el subárbol derecho
            node.right = self._insert_property(node.right, metric2, property_data)  # Insertar en el subárbol derecho con metric2

        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and metric1 < node.left.key:
            return self.rotate_right(node)

        if balance < -1 and metric1 > node.right.key:
            return self.rotate_left(node)

        if balance > 1 and metric1 > node.left.key:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and metric1 < node.right.key:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node
    

    def _convert_to_anytree(self, node):
        if node:
            new_node = Node(f"Key: {node.key}, Data: {node.data}")
            children = []

            if node.left:
                children.append(self._convert_to_anytree(node.left))
            if node.right:
                children.append(self._convert_to_anytree(node.right))

            new_node.children = children
            return new_node

    def print_tree(self):
        if self.root is not None:
            anytree_root = self._convert_to_anytree(self.root)
            for pre, fill, node in RenderTree(anytree_root):
                print(f"{pre}{node.name}")

    def delete_node_by_metric(self, metric):
        self.root = self._delete_node_by_metric(self.root, metric)

    def _delete_node_by_metric(self, node, metric):
        # Implementar la lógica para eliminar un nodo por métrica
        # Utiliza la lógica estándar de eliminación de un nodo en un árbol AVL
        if not node:
            return node

        if metric < node.key:
            node.left = self._delete_node_by_metric(node.left, metric)
        elif metric > node.key:
            node.right = self._delete_node_by_metric(node.right, metric)
        else:
            # Nodo encontrado, proceder con la eliminación
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Si el nodo tiene dos hijos, obtener el sucesor en orden
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.data = temp.data
            node.right = self._delete_node_by_metric(node.right, temp.key)

        # Actualizar la altura y equilibrar el árbol
        node.height = 1 + max(get_height(node.left), get_height(node.right))
        balance = get_balance_factor(node)

        if balance > 1 and get_balance_factor(node.left) >= 0:
            return self.rotate_right(node)

        if balance < -1 and get_balance_factor(node.right) <= 0:
            return self.rotate_left(node)

        if balance > 1 and get_balance_factor(node.left) < 0:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1 and get_balance_factor(node.right) > 0:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def search_node_by_metric(self, metric):
        return self._search_node_by_metric(self.root, metric)

    def _search_node_by_metric(self, node, metric):
        # Implementar la lógica para buscar un nodo por métrica
        if not node:
            return None

        if metric < node.key:
            return self._search_node_by_metric(node.left, metric)
        elif metric > node.key:
            return self._search_node_by_metric(node.right, metric)
        else:
            return node.data

    def search_nodes_by_criteria(self, criteria):
        nodes_found = []
        self._search_nodes_by_criteria(self.root, criteria, nodes_found)
        return nodes_found

    def _search_nodes_by_criteria(self, node, criteria, result):
        # Implementar la lógica para buscar nodos que cumplan con los criterios
        if not node:
            return

        if self._meets_criteria(node.data, criteria):
            result.append(node.data)

        if node.key >= criteria['min_metric']:
            self._search_nodes_by_criteria(node.left, criteria, result)
        if node.key < criteria['max_metric']:
            self._search_nodes_by_criteria(node.right, criteria, result)

    def _meets_criteria(self, data, criteria):
        # Implementar la lógica para verificar si un nodo cumple con los criterios
        if criteria['city'] and data['city'] != criteria['city']:
            return False
        if criteria['bedrooms'] and data['bedrooms'] < criteria['bedrooms']:
            return False
        if criteria['price'] and data['price'] > criteria['price']:
            return False
        return True

# Cargar el dataset desde el archivo CSV
df = pd.read_csv('co_properties_final.csv')

# Crear una instancia del Árbol AVL
avl_tree = AVLTree()

# Insertar cada propiedad en el árbol usando la métrica price / surface_total
for index, row in df.iterrows():
    avl_tree.insert_property(row.to_dict())

# Imprimir el árbol AVL en forma de árbol
avl_tree.print_tree()

while True:
    print("Menú:")
    print("1. Insertar un nodo")
    print("2. Eliminar un nodo por métrica")
    print("3. Buscar un nodo por métrica")
    print("4. Buscar nodos por criterios")
    print("5. Mostrar recorrido por niveles")
    print("6. Salir")

    choice = input("Ingrese su elección: ")

    if choice == "1":
        # Solicitar los datos necesarios al usuario
        key = float(input("Ingrese la métrica1: "))
        data = {
            'city': input("Ingrese la ciudad: "),
            'bedrooms': int(input("Ingrese el número de dormitorios: ")),
            'price': float(input("Ingrese el precio: ")),
            'surface_total': float(input("Ingrese la superficie total: ")),
            'bathrooms': int(input("Ingrese el número de baños: "))
        }

        # Llamar a la función insert_property
        avl_tree.insert_property({'price': data['price'], 'surface_total': data['surface_total'], 'bedrooms': data['bedrooms'], 'bathrooms': data['bathrooms'], 'city': data['city']})
        
        # Mostrar el árbol actualizado
        avl_tree.print_tree()
        
    elif choice == "2":
        # Solicitar la métrica por la cual desea eliminar el nodo
        metric_to_delete = float(input("Ingrese la métrica1 del nodo que desea eliminar: "))

        # Implementar la lógica para eliminar el nodo correspondiente
        avl_tree.delete_node_by_metric(metric_to_delete)
        
        # Mostrar el árbol actualizado
        avl_tree.print_tree()

    elif choice == "3":
        # Solicitar la métrica por la cual desea buscar el nodo
        metric_to_find = float(input("Ingrese la métrica1 del nodo que desea buscar: "))

        # Implementar la lógica para buscar y mostrar el nodo si se encuentra
        node_data = avl_tree.search_node_by_metric(metric_to_find)
        if node_data:
            print("Nodo encontrado:")
            print(node_data)
        else:
            print("Nodo no encontrado")

    elif choice == "4":
        # Solicitar los criterios al usuario (por ejemplo, ciudad, dormitorios, precio)
        city_criteria = input("Ingrese la ciudad (deje en blanco si no es un criterio): ")
        bedrooms_criteria = int(input("Ingrese el número de dormitorios (deje 0 si no es un criterio): "))
        price_criteria = float(input("Ingrese el precio máximo (deje 0 si no es un criterio): "))

        # Definir los criterios en un diccionario
        search_criteria = {
            'city': city_criteria,
            'bedrooms': bedrooms_criteria,
            'price': price_criteria,
            'min_metric': 0,  # Puedes ajustar estos valores según tu lógica
            'max_metric': float('inf')  # Puedes ajustar estos valores según tu lógica
        }

        # Buscar nodos que cumplan con los criterios
        nodes_found = avl_tree.search_nodes_by_criteria(search_criteria)

        # Mostrar los nodos encontrados
        if nodes_found:
            print("Nodos encontrados:")
            for node_data in nodes_found:
                print(node_data)
        else:
            print("Ningún nodo encontrado")

    elif choice == "5":
        # Mostrar el recorrido por niveles del árbol AVL
        avl_tree.print_tree()

    elif choice == "6":
        # Salir del programa
        break
    else:
        print("Opción no válida. Intente de nuevo.")
