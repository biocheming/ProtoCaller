import ProtoCaller.Utils.ConditionalList as _CondList
from . import Missing as _Missing


class Residue(_CondList.ConditionalList):
	# properties which have to be conserved within the whole residue
	_common_properties = ["chainID", "resName", "resSeq", "iCode"]
	# methods partially inherited from MissingResidue
	_inherited_methods = ["__copy__", "__deepcopy__", "__lt__", "__gt__", "__eq__", "__hash__", "type"]

	for method in _inherited_methods:
		vars()[method] = getattr(_Missing.MissingResidue, method)

	def __init__(self, atoms=None):
		if atoms is None:
			atoms = []
		super(Residue, self).__init__(atoms, self._checkAtom)

	def __getattr__(self, item):
		if item in self._common_properties:
			if not self.__len__():
				return None
			return getattr(self.__getitem__(0), item)

	def __setattr__(self, key, value):
		if key in self._common_properties:
			for atom in self.__iter__():
				setattr(atom, key, value)
		super(Residue, self).__setattr__(key, value)

	def __str__(self):
		return "".join([atom.__str__() for atom in self.__iter__()])

	def __repr__(self):
		return "<Residue of {} atoms>".format(self.__len__())

	def numberOfAtoms(self):
		return self.__len__()

	def reNumberAtoms(self, start=1, custom_serials=None):
		if custom_serials is None:
			serials = [start + i for i in range(start, start + self.__len__())]
		elif len(custom_serials) == self.__len__():
			serials = custom_serials
		else:
			raise ValueError("Custom number list does not match number of atoms")

		for i, atom in zip(serials, self):
			atom.serial = i

	def _checkAtom(self, atom):
		# checks whether the atom has the same chainID, resName, resSeq and iCode as the current object
		try:
			for prop in self._common_properties:
				if getattr(self, prop) is not None:
					assert (getattr(self, prop) == getattr(atom, prop))
		except AttributeError:
			raise TypeError("Need to pass a valid object with chainID, resSeq, resName and iCode attributes")
		except AssertionError:
			raise ValueError("Input atom(s) from an incompatible residue")