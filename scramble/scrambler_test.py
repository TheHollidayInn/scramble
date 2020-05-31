import cv2
import random
import numpy as np
import os
import pathlib
curr_path = pathlib.Path(__file__).parent.absolute()
pictures = [os.path.join(curr_path, "16.png")]
MOVE_UP = 0
MOVE_LEFT = 1
MOVE_DOWN = 2
MOVE_RIGHT = 3

class ImageScrambleGame:
	def __init__(self, gsize=4, img_path=os.path.join(curr_path, "16.png"), seednum=0):
		image = cv2.imread(img_path)
		self.parts = []
		self.gsize = gsize
		self.h, self.w, _ = image.shape
		self.ws = self.w // self.gsize
		self.hs = self.h // self.gsize
		for y in range(self.gsize):
			for x in range(self.gsize):
				part_num = self.get_part_num(x, y)
				self.parts.append([part_num, image[self.hs * y: self.hs * (y + 1),self.ws * x: self.ws * (x + 1)].copy(), False])

		random.seed(seednum)
		random.shuffle(self.parts)
		whitespot_idx = random.randint(0, self.gsize**2-1)#random.choice([0, (self.gsize - 1), self.gsize * (self.gsize - 1), self.gsize**2-1])
		
		part_to_remove = self.parts[whitespot_idx]
		self.parts[whitespot_idx] = [part_to_remove[0], np.zeros(part_to_remove[1].shape, dtype=np.uint8), True]
		if not self.solvability():
			raise Exception("Unsolvable.  Try new seed.")
		
	def _inversions(self):
		swap = 0
		for idx in range(self.gsize**2):
			part = self.parts[idx]
			if part[2]:
				continue
			num = part[0]
			for idx2 in range(idx, self.gsize**2):
				if idx2 == idx:
					continue
				part2 = self.parts[idx2]
				if part2[2]:
					continue
				if num > part2[0]:
					swap += 1
		return swap
		
	def solvability(self):
		is_odd = self.gsize % 2 != 0
		inversions = self._inversions()
		odd_num_inversions = inversions % 2 != 0
		_, y = self.get_grid_coord(self.whitespot_idx)
		blank_odd = ((self.gsize) - y) % 2 != 0
		solv = (is_odd and not odd_num_inversions) or (not is_odd and (blank_odd == (not odd_num_inversions)))
		return solv

	@property
	def whitespot_idx(self):
		return [i for i in range(len(self.parts)) if self.parts[i][2] == True][0]

	def get_part_num(self, x, y):
		return x + (y * self.gsize)

	def get_grid_coord(self, part_num):
		y = part_num // self.gsize
		x = part_num - (y * self.gsize)
		return (x, y)

	def _swap_parts(self, fidx,sidx):
		tmp = self.parts[fidx]
		self.parts[fidx] = self.parts[sidx]
		self.parts[sidx] = tmp

	def get_current(self):
		current_image = np.zeros([self.h,self.w,3], dtype=np.uint8)
		for y in range(self.gsize):
			for x in range(self.gsize):
				part_num = self.get_part_num(x, y)
				current_image[self.hs * y: self.hs * (y + 1),self.ws * x: self.ws * (x + 1)] = self.parts[part_num][1].copy()

		return current_image

	def get_state(self):
		state = []
		for y in range(self.gsize):
			state.append([])
			for x in range(self.gsize):
				part_num = self.get_part_num(x, y)
				state[y].append(self.parts[part_num][0] if not self.parts[part_num][2] else -1)

		return state

	def click_move(self, event, x, y, flags, param):
		if event == cv2.EVENT_LBUTTONDOWN:
			real_x = int(x * (self.w / 600))
			real_y = int(y * (self.h / 600))
			cuad_x = int((x / self.w) / (1.0/self.gsize))
			cuad_y = int((y / self.h) / (1.0/self.gsize))
			print('coords', cuad_x, cuad_y)
			ws_idx = self.whitespot_idx
			wx, wy = self.get_grid_coord(ws_idx)
			print("wscoords", wx, wy)
			diff_x = cuad_x - wx 
			diff_y = cuad_y - wy
			print(diff_x, diff_y)
			if diff_x == 0 and abs(diff_y) == 1 or (diff_y == 0 and abs(diff_x) == 1):
				part_num = self.get_part_num(cuad_x, cuad_y)
				self._swap_parts(ws_idx, part_num)


	def move_blank(self, movement):
		ws_idx = self.whitespot_idx
		x, y = self.get_grid_coord(ws_idx)
		if movement == MOVE_RIGHT and x < self.gsize-1:
			x+=1
		elif movement == MOVE_DOWN and y < self.gsize-1:
			y += 1
			
		elif movement == MOVE_UP and y > 0:
			y -= 1
		elif movement == MOVE_LEFT and x > 0:
			x -=1 

		part_num = self.get_part_num(x, y)
		self._swap_parts(self.whitespot_idx, part_num)


def demo():
	cv2.namedWindow('window',cv2.WINDOW_NORMAL)
	cv2.resizeWindow('window', 600, 600)
	isg = ImageScrambleGame(img_path=random.choice(pictures))
	cv2.setMouseCallback("window", isg.click_move)
	
	while True:
		k = cv2.waitKey(10) & 0xff
		if k == ord('w'):
			isg.move_blank(MOVE_UP)
		if k == ord('s'):
			isg.move_blank(MOVE_DOWN)
		if k == ord('a'):
			isg.move_blank(MOVE_LEFT)
		if k == ord('d'):
			isg.move_blank(MOVE_RIGHT)

		cv2.imshow('window',isg.get_current())

if __name__ == "__main__":
	demo()

	
	
