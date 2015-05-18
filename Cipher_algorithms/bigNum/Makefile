windowspy32: main.cpp bigNum.cpp
	swig -c++ -python bigNum.i
	g++ -c bigNum.cpp
	g++ -c bigNum_wrap.cxx -IC:\Python27\include
	g++ bigNum.o bigNum_wrap.o -Ic:\python27\include -Lc:\python27\libs -lpython27 -shared -o _bigNum.pyd
	del bigNum.o bigNum_wrap.cxx bigNum_wrap.o
	
windowspy64: main.cpp bigNumber.cpp
	swig -c++ -python bigNumber.i
	C:\TDM-GCC-64\bin\g++ -c bigNumber.cpp
	C:\TDM-GCC-64\bin\g++ -c bigNumber_wrap.cxx -IC:\Python27\include
	C:\TDM-GCC-64\bin\g++ bigNumber.o bigNumber_wrap.o -Ic:\python27\include -Lc:\python27\libs -lpython27 -shared -o _bigNumber.pyd
	del bigNumber.o bigNumber_wrap.cxx bigNumber_wrap.o
	
