
import datetime


# # Meu deus, como só isso tem 100 linhas??????

# class Node:

#     def __init__(self,Data = None):

#         self.data = Data
#         self.next = None


# class linkedList:

#     def __init__(self):

#         self.head = Node()
#         self.lenght = 0


#     def append(self,data):

#         cur = self.head
#         new_data = Node(data)

#         while cur.next != None:
#             cur = cur.next

#         self.lenght += 1
#         cur.next = new_data


#     def length(self):
#         return self.lenght

#     def value(self,user_index):

#         try:
#             if user_index > self.lenght:
#                 return "Erro out of index"
#         except TypeError:
#             return "TypeError: o argumento passado tem que ser um inteiro."

#         cur = self.head
#         cur_index = 0

#         while True:

#             cur = cur.next
#             if cur_index == user_index:
#                 return cur.data

#             cur_index += 1


#     def values(self):
#         cur = self.head
#         lista = []

#         while cur.next != None:
#             cur = cur.next
#             lista.append(cur.data)
#         return lista


#     def remove(self,user_index):
#         try:
#             if user_index > self.lenght:
#                 return "Erro out of index"
#         except TypeError:
#             return "TypeError: o argumento passado tem que ser um inteiro."

#         last_node = None
#         cur = self.head
#         cur_index = 0

#         while True:
#             last_node = cur
#             cur = cur.next
            
#             if cur_index == user_index:
#                 last_node.next = cur.next
#                 self.lenght -= 1
#                 return
            
#             cur_index += 1


# linked = linkedList()

# linked.append(1)
# linked.append(2)
# linked.append(3)
# print(linked.values())
# print(linked.remove(5))
# print(linked.values())

# print(linked.length())

data_agora=datetime.datetime.now()
print(data_agora.strftime("%Y-%m-%d"))