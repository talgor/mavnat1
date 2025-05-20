#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0
		self.amir = 0 # how manny of the nodes in the sub-tree have balance factor of 0
		
	def __repr__(self):  # can delete before uploading
		s = "key: " + str(self.key) + " value: " + str(self.value)
		return s

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.key == None:
			return False
		else:
			return True


	def add_virtual_childern(self):
		l = AVLNode(None, None)
		r = AVLNode(None, None)
		self.left = l
		self.right = r
		self.hight = 0
		self.size = 1
		self.amir = 1



"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		self.max = None


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		node = self.search_from_top(key, self.root)
		if node.is_real_node():
			return node
		else:
			return None


	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
    @param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	
	def search_from_top(self, key, top):
		node = top
		while node.key!=None:
			if node.key == key:
				return node
			elif key < node.key:
				node = node.left
			elif key > node.key:
				node = node.right
		return node


	def search_from_max(self, key):
		node = self.max
		while node.key!=None and node.key > key:
			node = node.parent
		return self.search_from_top(key, node)


	def insert(self, key, val, start="root"):
		if self.root == None:
			root = AVLNode(key, val)
			root.add_virtual_childern()
			self.root = root
			self.max = root
			return 0
		if start == "max":
			node = self.search_from_max(key)
		else:
			node = self.search_from_top(key, self.root)	
		node.key = key
		node.value = val
		node.add_virtual_childern()
		if key > self.max.key:
			self.max = node

		total_updates = self.travel_up_after_insert(node.parent)

		return total_updates


	def bypass(self, deleted, son):
		son.parent = deleted.parent
		if deleted.parent != None:
			if deleted.parent.left == deleted:
				deleted.parent.left = son
			else:
				deleted.parent.right = son
		else:
			self.root = son


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node): # not close to finished!
		l = node.left.is_real_node()
		r = node.right.is_real_node()
		rebalance_from = node
		if l and r:
			suc = self.successor(node)
			self.bypass(suc, suc.right)
			rebalance_from = suc.parent
			self.replace_node(node, suc)
		if l:
			self.bypass(node, node.left)	
			rebalance_from = node.parent
		else: #if node is a leaf, will replace node with it's right virtual leaf
			self.bypass(node, node.right)
			rebalance_from = node.parent #what if it is the root? and there is no parent?
		total_updates = self.travel_up_after_delete(rebalance_from)
		return total_updates

	def replace_node(self, replaced, replacer):
		self.bypass(replaced, replacer) #sorts the pointers to and from the parent
		replacer.right = replaced.right
		replacer.left = replaced.left
		replacer.right.parent = replacer
		replacer.left.parent = replacer
		replacer.hight = replaced.hight
		replacer.size = replaced.size
		replacer.amir = replaced.amir

	def rec_in_order(self, node, l):
		if node.is_real_node() == False:
			return
		self.rec_in_order(node.left, l)
		l.append((node.key, node.value)) #will always happend in order, because of the command order
		self.rec_in_order(node.right, l) 

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		ordered = []
		if self.root != None:
			self.rec_in_order(self.root, ordered)
		return ordered


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		if self.root == None:
			return 0
		return self.root.size


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root


	"""gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		if self.root == None:
			return 0
		return self.root.amir / self.root.size
	
	def balance_factor(self, node):
		return node.left.height - node.right.height
	
	def successor(self, node):
		if node.right.is_real_node():
			min = node.right
			while min.left.is_real_node():
				min = min.left
			return min
		
		success = node.parent
		while success != None and node == success.right:
			node = success
			success = node.parent
		return success

	def predecessor(self, node):
		if node.left.is_real_node():
			max = node.left
			while max.right.is_real_node():
				max = max.right
			return max
		
		pred = node.parent
		while pred != None and node == pred.left:
			node = pred
			pred = node.parent
		return pred
	
	def travel_up_after_insert(self, node):
		# total rotations and height changes
		total_updates = 0

		rotation_done = False

		while node:
			total_updates += self.update(node)
			bf = self.balance_factor(node)

			if not rotation_done and abs(bf) > 1:
				(new_root, rot) = self.rebalance(node)
				total_updates += rot
				if new_root.parent is None:
					self.root = new_root
				rotation_done = True

			node = node.parent
		
		return total_updates

	def travel_up_after_delete(self, node):
		# total rotations and height changes
		total_updates = 0

		while node:
			total_updates += self.update(node)
			bf = self.balance_factor(node)

			if abs(bf) > 1:
				(new_root, rot) = self.rebalance(node)
				total_updates += rot
				if new_root.parent is None:
					self.root = new_root

			node = node.parent

		return total_updates

	def update(self, node):
		curr_height = node.height
		node.height = 1 + max(self.height(node.left), self.height(node.right))
		node.size = 1 + self.size(node.left) + self.size(node.right)

		#update Amir balance factor
		node.amir = node.left.amir + node.right.amir
		if self.balance_factor(node) == 0:
			node.amir += 1

		if curr_height != node.height:
			return 1
		return 0

	def rotate_right(self, node):
		# chat's fixes
		b = node
		a = b.left
		b.left = a.right
		if a.right:
			a.right.parent = b

		a.right = b
		a.parent = b.parent

		if b.parent:
			if b.parent.left == b:
				b.parent.left = a
			else:
				b.parent.right = a
		else:
			self.root = a

		b.parent = a

		num_height_updates = 0
		num_height_updates += self.update(b)
		num_height_updates += self.update(a)
		return (a, num_height_updates)

		# tal's version
		# b = node
		# is_left_child = False

		# if b.parent.left == b:
		# 	is_left_child = True

		# a = b.left
		# b.left = a.right
		# b.left.parent = b
		# a.right = b
		# a.parent = b.parent

		# if is_left_child:
		# 	a.parent.left = a
		# else:
		# 	a.parent.right = a
		
		# b.parent = a
		
		# self.update(b)
		# self.update(a)


	def rotate_left(self, node):
		# chat's fixes
		b = node
		a = b.right
		b.right = a.left
		if a.left:
			a.left.parent = b

		a.left = b
		a.parent = b.parent

		if b.parent:
			if b.parent.right == b:
				b.parent.right = a
			else:
				b.parent.left = a
		else:
			self.root = a

		b.parent = a

		num_height_updates = 0
		num_height_updates += self.update(b)
		num_height_updates += self.update(a)
		return (a, num_height_updates)
	
		# tal's version
		# b = node
		# is_right_child = False

		# if b.parent.right == b:
		# 	is_right_child = True

		# a = b.right
		# b.right = a.left
		# b.right.parent = b
		# a.left = b
		# a.parent = b.parent

		# if is_right_child:
		# 	a.parent.right = a
		# else:
		# 	a.parent.left = a
		
		# b.parent = a

		# self.update(b)
		# self.update(a)

	def rebalance(self, node):
		updates = 0
		# chat's fixes
		updates += self.update(node)
		bf = self.balance_factor(node)
		
		if bf > 1:
			if self.balance_factor(node.left) < 0:
				(node.left, num_updates) = self.rotate_left(node.left)
				updates += 1+num_updates
				node.left.parent = node

			(new_root, num_updates) = self.rotate_right(node)
			updates += 1+num_updates
			return (new_root, updates)

		if bf < -1:
			if self.balance_factor(node.right) > 0:
				(node.right, num_updates) = self.rotate_right(node.right)
				updates += 1+num_updates
				node.right.parent = node

			(new_root, num_updates) = self.rotate_left(node)
			updates += 1+num_updates
			return (new_root, updates)
		
		return (node, updates)



		# tal's version
		# self.update(node)
		# bf = self.balance_factor(node)
		
		# if bf > 1:
		# 	left_bf = self.balance_factor(node.left)
		# 	if left_bf == -1:
		# 		node.left = self.rotate_left(node.left)
		# 	self.rotate_right(node)
		# 	return

		# if bf < -1:
		# 	right_bf = self.balance_factor(node.right)
		# 	if right_bf == 1:
		# 		node.right = self.rotate_right(node.right)
		# 	self.rotate_left(node)
		# 	return

if __name__ == '__main__':
	tree = AVLTree()
	tree.insert(10, "ten")
	tree.insert(20, "twenty")
	tree.insert(5, "five")
	print(tree.avl_to_array())