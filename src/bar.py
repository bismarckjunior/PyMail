#-*-coding: utf-8-*-
"""
Copyright [2018] [Souza Jr, B. G.]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Bismarck Gomes Souza Junior <bismarckgomes@gmail.com>
About:  Functions that manager a progress bar
"""
import sys
from math import log10
sys.stdout.flush()


class ProgressBar:

	def __init__(self, end=100, name='', width=50, init=True, perc=True):
		"""
		@brief   Constructs the object.

		@param   end    Maximum value of progress bar
		@param   name   Name of progress bar
		@param   width  With of progress bar
		@param   init   Draw progress bar
		"""
		self.wbar_ = width
		# self.fmt_bar2_ = "{:s}[{:%ss}] {:s}%%" % self.wbar_
		self.name_ = name
		self.perc_ = perc


		self.set_end(end)

		if (init is True):
			self.init_bar()

	def init_bar(self, end=None):
		"""
		@brief   Initialize progress bar.

		@param   end   Maximum value of progress bar
		"""
		if (end is not None):
			self.end_ = end
		self.__draw_bar(0)

	def reset_bar(self, end=None):
		"""
		@brief   Reset progress bar.

		@param   end   Maximum value of progress bar
		"""
		if (end is not None):
			self.end_ = end
		self.draw_bar(0)

	def set_end(self, end):
		"""
		@brief   Change maximum value of progress bar.

		@param   end   Maximum value of progress bar
		"""
		if (end <= 0 ):
			raise Exception(60, "Invalid value in progress bar (end=%s)" % str(end))

		ndig = int(log10(end))+1

		if (self.perc_ is True):
			self.fmt_bar_ = "{:s}[{:%ds}] {:3d}%%" % self.wbar_
			self.len_detail_ = 4
			self.__draw_bar = self.__draw_bar_perc
		else:
			self.fmt_bar_ = "{:s}[{:%ds}] {:%dd}/%d" % (self.wbar_, ndig, end)
			self.len_detail_ = 2*ndig+1
			self.__draw_bar = self.__draw_bar_number

		self.end_ = end

	def update(self, pos):
		"""
		@brief   Update progress bar.

		@param   pos   Position in progress bar
		"""
		self.clear_bar()
		if (pos < 0): pos = 0
		if (pos > self.end_): pos = self.end_
		self.__draw_bar(pos)

	def __draw_bar_perc(self, pos):
		"""
		@brief   Draw progress bar without cleaning.

		@param   pos   Position in progress bar
		"""
		frac = float(pos)/self.end_
		print self.fmt_bar_.format(self.name_, '='*int(self.wbar_*frac), int(100*frac)),
		sys.stdout.flush()

	def __draw_bar_number(self, pos):
		frac = float(pos)/self.end_
		print self.fmt_bar_.format(self.name_, '='*int(self.wbar_*frac), pos),
		sys.stdout.flush()

	def clear_bar(self):
		"""
		@brief   Clear progress bar.
		"""
		sys.stdout.write('\b'*(self.wbar_+len(self.name_)+3+self.len_detail_))
		sys.stdout.flush()


if __name__ == '__main__':
	import time

	n = 50
	pb = ProgressBar(n, name='Progresso: ')#, perc=False)
	time.sleep(1)
	for i in range(n+1):
		pb.update(i)
		time.sleep(0.1)

	raw_input()
