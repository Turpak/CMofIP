#pragma once
#include <iostream>

#define BASE 1000000000
#define DIV_BY_ZERO 1

class bigNum
{
private:
	int _sign;

public:
	bigNum();
	bigNum(const char* String);
	bigNum(const bigNum& RightHandValue);
	bigNum(long long int RightHandValue);
	~bigNum();

	char* getString();
	char* __str__(); // для вывода числа в Python
	char* __repr__();
	bool getNum_From_txt(const char* FileName);
	bool saveNum_To_txt(const char* FileName);
	bool getNum_From_binfile(const char* FileName);
	bool saveNum_To_binfile(const char* FileName);


	bigNum& operator=(const bigNum& RightHandValue);

	bigNum operator+(const bigNum& right) const;
	bigNum operator-() const;
	bigNum operator-(const bigNum& right) const;
	bigNum operator*(const bigNum& right) const;
	bigNum operator/(const bigNum& right) const;
	bigNum operator%(const bigNum& right) const;
	bigNum& operator^(const bigNum& right) const;


	bool operator>(const bigNum& B);
	bool operator>=(const bigNum& B);
	bool operator<(const bigNum& B);
	bool operator<=(const bigNum& B);
	bool operator==(const bigNum& B);
	bool operator!=(const bigNum& B);

	// перегрузка операторов для Python
	bigNum operator+(const int& right) const;
	bigNum operator-(const int& right) const;
	bigNum operator*(const int& right) const;
	bigNum operator/(const int& right) const;
	bigNum operator%(const int& right) const;

	bool operator>(const int& B);
	bool operator>=(const int& B);
	bool operator<(const int& B);
	bool operator<=(const int& B);
	bool operator==(const int& B);
	bool operator!=(const int& B);
	
	bool Odd();
	
	friend std::ostream& operator<<(std::ostream &out, bigNum A);
	friend std::istream& operator>>(std::istream &is, bigNum &A);

	unsigned int* _digits;
	int _size;
	void _setSize(int size);
	void _DelZeroes();
	
private:
	unsigned int & operator[](int i);
	unsigned int operator[](int i) const;
	void _copy(const bigNum &rhv);
	long long int _compare(const bigNum& B);
	void _shiftLeft(int s);


	bigNum _sumAndSub(const bigNum& left, const bigNum& right) const;
	bigNum _multiplication(const bigNum A, const bigNum B) const;
	bigNum _dividing(const bigNum& A, const bigNum& B, bigNum &remainder) const;

};

void go_generate();

bigNum to_pow(const bigNum& A, const bigNum& B, bigNum& modulus);

bigNum random_big(bigNum max_value);

bigNum random_fixlen(int len);
