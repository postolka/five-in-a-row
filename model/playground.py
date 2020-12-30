from collections import deque
from enum import IntEnum, Enum


class Player(Enum):
	Me = False
	Opponent = True


class Direction(IntEnum):
	H = 0
	V = 1
	U = 2 # /
	D = 3 # \


class Move:
	player: Player
	x: int
	y: int

	def __init__(self, player: Player, x: int, y: int):
		self.player = player
		self.x = x
		self.y = y

	def __str__(self):
		return "[{: 3},{: 3}]:{}".format(self.x, self.y, "X" if self.player == Player.Me else "O")

	def coord(self, direction: Direction) -> int:
		return self.y if direction == Direction.H else self.x


class Candidate:
	direction: Direction
	moves: deque[Move] = deque[Move]()
	_a: int
	_b: int

	def __init__(self, move: Move, direction: Direction):
		self.moves.append(move)
		self.direction = direction
		# store start/end position - for -/\ use X coordinate, for | use Y one
		self._b = self._a = move.coord(self.direction)

	def append(self, move: Move) -> bool:
		coord = move.coord(self.direction)
		if (coord + 1) == self._a:	# add to the start
			self.moves.appendleft(move)
			return True
		if (coord - 1) == self._b:	# add to the end
			self.moves.append(move)
			return True
		return False	# doesn't connect

	def __len__(self):
		return len(self.moves)


class Dimension:
	_a: int
	_b: int

	def __init__(self, coord: int):
		self._a = self._b = coord

	def extend(self, coordinate: int):
		self._a = min(coordinate, self._a)
		self._b = max(coordinate, self._b)

	def __iter__(self):
		pos = self._a
		while pos <= self._b:
			yield pos
			pos += 1


class Playground:
	moves: set[Move]() = set[Move]()
	opportunities: set[Candidate]() = set[Candidate]()
	threats: set[Candidate]() = set[Candidate]()

	_w: Dimension
	_h: Dimension

	def play(self, move: Move):
		if len(self.moves):
			self._w.extend(move.x)
			self._h.extend(move.y)
		else:
			self._w = Dimension(move.x)
			self._h = Dimension(move.y)
		self.moves.add(move)
		self._update_candidates(self.opportunities if move.player == Player.Me else self.threats, move)

	@staticmethod
	def _update_candidates(candidates: set[Candidate], move: Move):
		added: bool = False
		for candidate in candidates:
			added |= candidate.append(move)
		if not added:
			for direction in Direction:
				candidates.add(Candidate(move, direction))

	def __str__(self):
		rows = dict[int, dict[int, Player]]()
		for move in self.moves:
			if move.y in rows.keys():
				rows[move.y][move.x] = move.player
			else:
				rows[move.y] = {	move.x: move.player}
		field: str = ""
		for y in self._h:
			if y in rows.keys():
				for x in self._w:
					field += ("X" if rows[y][x] == Player.Me else "O") if x in rows[y].keys() else " "
			field += "\n"
		return field
