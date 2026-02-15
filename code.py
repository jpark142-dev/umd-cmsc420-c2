# BST Variation 1
# Contains values.
# Has a restructure which works like that for a scapegoat tree, but this is on-demand only.

from __future__ import annotations
from typing import List
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  age        : int  = None,
                  rownumbers : List[int] = [],
                  leftchild  : Node = None,
                  rightchild : Node = None,
                  parent     : Node = None,
                  iop        : Node = None,
                  ios        : Node = None):
        self.age        = age
        self.rownumbers = rownumbers
        self.leftchild  = leftchild
        self.rightchild = rightchild
        self.parent     = parent
        self.ios        = ios
        self.iop        = iop

# The class for a database.
class DB():
    # The __init__
    # DO NOT MODIFY!
    def __init__(self,
                 rows : List[List] = [],
                 root : Node = None
                 ):
        self.rows = rows
        self.root = root

    # Dump the rows of the database.
    # DO NOT MODIFY!
    def dump_rows(self) -> str:
        return('\n'.join( [f'{i},{l[0]},{l[1]}' for i,l in enumerate(self.rows)]))

    # Dump the index of the database.
    # DO NOT MODIFY!
    def dump_index(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "age"        : node.age,
                "rownumbers" : str(node.rownumbers),
                "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
                "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None),
                "parent-age" : node.parent.age if node.parent is not None else None,
                "iop-age"    : node.iop.age if node.iop is not None else None,
                "ios-age"    : node.ios.age if node.ios is not None else None
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent = 2)

    # Insert a row into the database and update the index.
    def insert(self,name: str, age: int):
        self.rows.append([name, age])
        row_num = len(self.rows) - 1

        if self.root is None:
            self.root = Node(age= age, rownumbers= [row_num])
        else:
            self._insert_node(self.root, age, row_num)
    
    # Helper function for insert
    def _insert_node(self, current, age, row_num):
        # Connect the parent node with the inserting node in leftchild position
        if age < current.age:
            if current.leftchild is None:
                new_node = Node(age= age, rownumbers= [row_num])
                new_node.parent = current
                current.leftchild = new_node
                new_node.ios = current
                new_node.iop = current.iop
                if current.iop is not None:
                    current.iop.ios = new_node
                current.iop = new_node
            # Refind the place for inserting in leftchild position
            else:
                self._insert_node(current.leftchild, age, row_num)
        # Connect the parent node with the inserting node in rightchild position
        elif age > current.age:
            if current.rightchild is None:
                new_node = Node(age= age, rownumbers= [row_num])
                new_node.parent = current
                current.rightchild = new_node
                new_node.iop = current
                new_node.ios = current.ios
                if current.ios is not None:
                    current.ios.iop = new_node
                current.ios = new_node
            # Refind the place for inserting in rightchild position
            else:
                self._insert_node(current.rightchild, age, row_num)
        # If inserting age is same with current's age then just adding the rownumber
        else:
            current.rownumbers.append(row_num)


    # Delete a row from the database and update the index.
    def delete(self,name:str):
        # Search through self.rows to find the row number and age of corresponding name
        row_num = None
        for i in range(len(self.rows)):
            if self.rows[i][0] == name:
                row_num = i
                age = self.rows[i][1]
                break
        
        # Use helper function to find the node in BST
        node = self._find_node(self.root, age)

        # If there's more than one row_num in rownumbers then just remove only the row num, not Node
        if len(node.rownumbers) > 1:
            node.rownumbers.remove(row_num)
        else:
            #Unlink the node itself first from the iop/ios pointer such as removing from a double-linked list
            if node.iop is not None:
                node.iop.ios = node.ios
            if node.ios is not None:
                node.ios.iop = node.iop
            
            # Case 1: if there's no childs (No leaf) just delete the node
            if node.leftchild is None and node.rightchild is None:
                if node.parent == None:
                    self.root = None
                elif node.parent.leftchild == node:
                    node.parent.leftchild = None
                else:
                    node.parent.rightchild = None
            # Case 2-a: if the node has one child in leftchild, replace the node's left children to its place 
            elif node.leftchild is not None and node.rightchild is None:
                child = node.leftchild
                child.parent = node.parent
                if node.parent == None:
                    self.root = child
                elif node.parent.leftchild == node:
                    node.parent.leftchild = child
                else:
                    node.parent.rightchild = child
            # Case 2-b: if the node has one child in rightchild, replace the node's right children to its place 
            elif node.rightchild is not None and node.leftchild is None:
                child = node.rightchild
                child.parent = node.parent
                if node.parent == None:
                    self.root = child
                elif node.parent.leftchild == node:
                    node.parent.leftchild = child
                else:
                    node.parent.rightchild = child
            # Case 3: if the node has two children, we need to replace with inorder prodecessor        
            else:
                pred = node.iop
                node.age = pred.age
                node.rownumbers = pred.rownumbers

                if pred.iop is not None:
                    pred.iop.ios = node
                node.iop = pred.iop
                if node.ios is not None:
                    node.ios.iop = node

                if pred.leftchild is None:
                    if pred.parent.leftchild == pred:
                        pred.parent.leftchild = None
                    else:
                        pred.parent.rightchild = None
                else:
                    child = pred.leftchild
                    child.parent = pred.parent
                    if pred.parent.leftchild == pred:
                        pred.parent.leftchild = child
                    else:
                        pred.parent.rightchild = child
        # Remove the row and update row number after delete node
        self.rows.pop(row_num)
        self._update_rownumbers(self.root,row_num)

    # Helper function which is finding a specific node for delete function
    def _find_node(self, current, age):
        if current is None:
            return None
        if age < current.age:
            return self._find_node(current.leftchild, age)
        elif age > current.age:
            return self._find_node(current.rightchild, age)
        else:
            return current

    # After the delete, we need to update deleted node's information to row 
    def _update_rownumbers(self, current, deleted_row):
        if current is None:
            return current
        updated = []
        for r in current.rownumbers:
            if r > deleted_row:
                updated.append(r-1)
            else:
                updated.append(r)
        current.rownumbers = updated
        self._update_rownumbers(current.leftchild, deleted_row)
        self._update_rownumbers(current.rightchild, deleted_row)

    # Use the index to find a the people whose age is specified.
    def people_single(self,age:int):
        # Replace these lines.
        # d should be the depth of the node where the names are found.
        # n should be the list of names.
        node = self._find_node(self.root, age)
        d = self._find_depth(self.root, age)
        # Get names from row numbers
        n = [self.rows[r][0] for r in node.rownumbers]
        # Return the object.
        n.sort()
        r = {'depth' : d,'names': n }
        return json.dumps(r,indent = 2)
    
    # Finding the node's depth in BST with recursion
    def _find_depth(self, current, age, depth =0):
        if current.age is None:
            return -1
        if age < current.age:
            return self._find_depth(current.leftchild, age, depth + 1)
        elif age > current.age:
            return self._find_depth(current.rightchild, age, depth + 1)
        else:
            return depth
        

    # Use the index to find a the people whose age is in the range given.
    def people_range(self,age_min:int,age_max:int):
        # Replace these lines.
        # d should be the number of nodes where the names are found.
        # n should be the list of names.
        n = []
        d = self._find_people(self.root, age_min, age_max, n)
        # Return the object.
        n.sort()
        r = {'nodecount' : d,'names': n }
        return json.dumps(r,indent = 2)
    
    # count people who in range from age_min to age_max and collect names into the list
    def _find_people(self, current, age_min, age_max, n):
        if current is None:
            return 0
        count = 0
        if current.age < age_min:
            count += self._find_people(current.rightchild, age_min, age_max, n)
        elif current.age > age_max:
            count += self._find_people(current.leftchild, age_min, age_max, n)
        else:
            count += 1
            for r in current.rownumbers: 
                n.append(self.rows[r][0])
            count += self._find_people(current.leftchild, age_min, age_max, n)
            count += self._find_people(current.rightchild, age_min, age_max, n)
        return count