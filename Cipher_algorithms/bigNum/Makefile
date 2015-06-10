all:
	swig -c++ -python bigNum.i
	g++ -fPIC -c bigNum.cpp
	g++ -fPIC -c bigNum_wrap.cxx -I/usr/include/python2.7
	g++ -shared bigNum.o bigNum_wrap.o -o _bigNum.so
	rm *.o *.cxx
