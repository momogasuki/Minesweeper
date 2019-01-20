import cv2,os
from numpy import *
from sklearn.metrics import mean_squared_error
from scipy.special import comb, perm

# Bule, Green, Red #

class Board:
	def __init__(self,img,match_dict,remain_num):
		self.img_raw = img[10:-10,10:-10]
		self.match_dict = match_dict
		self.step = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
		self.remain_num = remain_num
	
	def createBoard(self):
		img2 = cv2.cvtColor(self.img_raw,cv2.COLOR_BGR2GRAY)
		stat = zeros_like(img2,dtype=float32)
		idx = argwhere(img2<20)
		Umost,Lmost = idx[0]
		Dmost,Rmost = idx[-1]
		stat[where(img2<50)] = 1
		#printimage(255-stat*255)
		
		self.row_cnt = self.col_cnt = 0
		self.row_edge, self.col_edge = [], []
		sum_row = sum(stat,axis=1)
		row = where(sum_row>200)[0]
		for i in range(row.size-1):
			if row[i+1]-row[i] > 5:
				self.row_cnt += 1
				self.row_edge.append(row[i])
		self.row_edge.append(row[-1])
		sum_col = sum(stat,axis=0)
		col = where(sum_col>150)[0]
		for i in range(col.size-1):
			if col[i+1]-col[i] > 5:
				self.col_cnt += 1
				self.col_edge.append(col[i])
		self.col_edge.append(col[-1])
		
		self.map = zeros((self.row_cnt,self.col_cnt))
		for r in range(self.row_cnt):
			for c in range(self.col_cnt):
				grid = self.getGrid(r,c)
				self.map[r,c] = match(grid,self.match_dict)
				#printimage(grid)
		#print(self.map)
		
	def getGrid(self,r,c):
		if r<0 or c<0 or r>=self.row_cnt or c>=self.col_cnt:
			print('Error: Grid index out of range!')
			exit()
		grid = self.img_raw[self.row_edge[r]:self.row_edge[r+1],self.col_edge[c]:self.col_edge[c+1]]
		grid = normed_image(grid)
		return grid
		
	def doSomething(self):
		self.unexp_all = argwhere(self.map==-2)
		self.unexp_edge = []
		for r,c in self.unexp_all:
			for dr,dc in self.step:
				if not self.isValid(r+dr,c+dc): continue
				if self.map[r+dr,c+dc]>=0:
					self.unexp_edge.append((r,c))
					break
		self.unexp_edge_num = len(self.unexp_edge)
		self.unexp_inside_num = len(self.unexp_all) - self.unexp_edge_num
		self.case_all = zeros(self.unexp_edge_num)
		self.case_ima = zeros(self.unexp_edge_num)
		self.case_num = 0
		self.inside_all_num = 0
		self.dfs(0,self.remain_num)
		#print(self.unexp_edge)
		for i in range(self.unexp_edge_num):
			self.drawCircle(self.unexp_edge[i],self.case_all[i]/self.case_num)
			#print('({},{}): {}'.format(self.unexp_edge[i][0],self.unexp_edge[i][1],self.case_all[i]/self.case_num))
		#print('inside grid: {}'.format(self.inside_all_num/(self.case_num*self.unexp_inside_num)))
		for r,c in self.unexp_all:
			if (r,c) in self.unexp_edge: continue
			self.drawCircle((r,c),self.inside_all_num/(self.case_num*self.unexp_inside_num))
		printimage(self.img_raw)
		
	def isValid(self,r,c):
		return r>=0 and c>=0 and r<self.row_cnt and c<self.col_cnt
		
	def dfs(self,n,rem):
		if n == self.unexp_edge_num:
			self.inside_all_num += rem*comb(self.unexp_inside_num,rem)
			self.case_num += comb(self.unexp_inside_num,rem)
			self.case_all += comb(self.unexp_inside_num,rem)*self.case_ima
			return
		if self.unexp_edge_num-n+self.unexp_inside_num < rem:
			return
		self.map[self.unexp_edge[n]] = -3 # is mine
		self.case_ima[n] = 1
		if self.check(self.unexp_edge[n]) and rem:
			#print((n,1))
			self.dfs(n+1,rem-1)
		self.map[self.unexp_edge[n]] = -4 # not mine
		self.case_ima[n] = 0
		if self.check(self.unexp_edge[n]):
			#print((n,0))
			self.dfs(n+1,rem)
		self.map[self.unexp_edge[n]] = -2
		
	def check(self,codi):
		r,c = codi
		for dr,dc in self.step:
			if not self.isValid(r+dr,c+dc): continue
			if self.map[r+dr,c+dc]<0: continue
			cnt = 0
			undecided = 0
			for ddr,ddc in self.step:
				if not self.isValid(r+dr+ddr,c+dc+ddc): continue
				if self.map[r+dr+ddr,c+dc+ddc] in {-1,-3}: cnt += 1
				if self.map[r+dr+ddr,c+dc+ddc] == -2: undecided += 1
			if self.map[r+dr,c+dc] not in range(cnt,cnt+undecided+1): return False
		return True
	
	def drawCircle(self,codi,p):
		r,c = codi
		y = (self.row_edge[r]+self.row_edge[r+1])//2
		x = (self.col_edge[c]+self.col_edge[c+1])//2
		G = (1-p)*255
		cv2.circle(self.img_raw,(x,y), 10, (0,G,255-G), -1)
		
def normed_image(img):
	return cv2.resize(img,(10,10),cv2.INTER_AREA)

def printimage(img):
	cv2.namedWindow('image',cv2.WINDOW_NORMAL)
	cv2.imshow('image',img)
	k = cv2.waitKey(0)
	if k == ord('s'):
		cv2.imwrite('out.png',img)
	cv2.destroyAllWindows()
	
def RGB_err(img1,img2):
	err0 = mean_squared_error(img1[:,:,0],img2[:,:,0])
	err1 = mean_squared_error(img1[:,:,1],img2[:,:,1])
	err2 = mean_squared_error(img1[:,:,2],img2[:,:,2])
	return err0+err1+err2
	
def match(grid,match_dict):
	grid = grid.astype(int)
	ERRmin = 2147483646
	ERRmin2 = 2147483647
	match1 = match2 = ''
	for label,img in match_dict.items():
		err = RGB_err(grid[1:-1,1:-1],normed_image(img).astype(int)[1:-1,1:-1])
		if err < ERRmin:
			ERRmin2 = ERRmin
			ERRmin = err
			match2 = match1
			match1 = label
		elif err < ERRmin2:
			ERRmin2 = err
			match2 = label
		#print('{}: {}'.format(label,err))
	
	#print('{}: {}'.format(match1,ERRmin))
	#print('{}: {}'.format(match2,ERRmin2))
	#print('')
	stat = match1.split('_')[0]
	if stat == 'unexplored': return -2
	if stat == 'flag': return -1
	if stat == 'empty': return 0
	return int(stat)

if __name__ == '__main__':
	# 这里的目的是读入所有基准栅格，用来比对的 #
	match_dict = {}
	for a,b,c in os.walk('match'):
		for filename in c:
			path = a + '/' + filename
			match_img = cv2.imread(path,True)
			match_img = normed_image(match_img)
			match_dict[filename] = match_img

	img = cv2.imread('1547914941(1).png',True)
	board = Board(img,match_dict,6)
	board.createBoard()
	board.doSomething()