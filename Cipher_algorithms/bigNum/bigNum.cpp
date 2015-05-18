#include "bigNum.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>
#include <time.h>
using std::ifstream;
using std::ofstream;

bigNum::bigNum()
{
	this->_size = 1;
	this->_sign = 0;
	this->_digits = new unsigned int[1];
	this->_digits[0] = 0;
}

bigNum::bigNum(const char* string) 
{

	if (!string)
		return;

	this->_size = 0;

	int strSize = strlen(string);
	int strSign = 0;
	if (string[0] == '-')
	{
		strSize--;
		strSign = 1;
	}

	const char* pStr = string + strSign;
	while (*pStr)
	{
		if (*pStr < '0' || *pStr > '9')
		{
			this->_size = 0;
			_setSize(1);
			return;
		}
		pStr++;
	}

	this->_setSize((strSize + strSign + 8) / 9); 

	for (int i = 0; i < (strSize + strSign) / 9; i++)
	{
		pStr -= 9;
		char splStr[10];
		memcpy(splStr, pStr, 9);
		splStr[9] = '\0'; 
		unsigned int digitI = atol(splStr);
		this->_digits[i] = digitI;
	}

	char ost[10];
	memset(ost, 0, 10);
	memcpy(ost, string + strSign, pStr - string - strSign);
	if (strlen(ost) > 0)
	{
		unsigned int lastDigit = atol(ost);
		this->operator[](-1) = lastDigit;
	}

	this->_sign = strSign;
	this->_DelZeroes();
}

bigNum::bigNum(const bigNum &rhv)
{
	_copy(rhv);
}

bigNum::bigNum(long long int value)
{
	this->_digits = new unsigned int[3]();
	this->_size = 0;
	this->_sign = 0;
	long long int carry = value;
	if (carry < 0)
	{
		this->_sign = 1;
		carry = -carry;
	}
	do
	{
		this->_size++;
		this->_digits[this->_size - 1] = carry % BASE;
		carry = carry / BASE;
	} while (carry);
}

bigNum::~bigNum()
{
	if (this->_size) delete[] _digits;
}


char* bigNum::getString()
{
  char* strBuffer = new char[this->_size * 9 + 1 + this->_sign]();
	char* pString = strBuffer + this->_size * 9 + this->_sign;

	for (int i = 0; i < this->_size; i++)
	{
		char splStr[10];
		sprintf(splStr, "%09u", this->_digits[i]);

		pString -= 9;
		memcpy(pString, splStr, 9);
	}

	while (*pString == '0' && *(pString + 1))
		pString++;

	if (this->_sign)
	{
		pString--;
		*pString = '-';
	}

	char* str = new char[strlen(pString) + 1]();
	strcpy(str, pString);
	delete[] strBuffer;

	return str;
}

bool bigNum::getNum_From_txt(const char* filename)
{
	ifstream Text_file(filename);
	if (Text_file.fail())
		return false;

	Text_file.seekg(0, std::ios::end);
	int SizeOfFile = Text_file.tellg();
	Text_file.seekg(0, std::ios::beg);

	char* string = new char[SizeOfFile + 1]();
	Text_file >> string;
	Text_file.close();

	*this = bigNum(string);
	delete[] string;
	return true;
}

bool bigNum::saveNum_To_txt(const char* filename)
{
	ofstream Result_file(filename);
	if (Result_file.fail())
		return false;

	char* string = this->getString();
	Result_file << string;
	delete[] string;
	Result_file.close();

	return true;
}

bool bigNum::saveNum_To_binfile(const char* filename)
{
	getString();

	ofstream Result_file(filename, std::ios::binary);
	if (Result_file.fail())
		return false;
	
	bigNum temp = *this;
	bigNum b256 = 256;
	bigNum b0 = (long long int)0;

	while (temp != b0)
	{
		bigNum remainder;
		temp = _dividing(temp, b256, remainder);
		remainder.getString();

		unsigned char ost = remainder[0];
		Result_file.write( (char*) &ost, 1);
	}

	Result_file.close();
	return true;
}

bool bigNum::getNum_From_binfile(const char* filename)
{
  ifstream Bin_file(filename, std::ios::binary);

	if (Bin_file.fail())
		return false;

	Bin_file.seekg(0, std::ios::end);
	int SizeOfFile = Bin_file.tellg();
	Bin_file.seekg(0, std::ios::beg);

	unsigned char* fileContent = new unsigned char[SizeOfFile];
	Bin_file.read((char*) fileContent, SizeOfFile);
	Bin_file.close();

	bigNum res;
	bigNum b256 = 256;
	for (int i = 0; i < SizeOfFile; i++)
	{
		res = res * b256;
		res = res + fileContent[i];
	}

	*this = res;
	return true;
}


void bigNum::_setSize(int size)
{	 
	if (this->_size)
		delete[] this->_digits;
	if (size == 0)
		size = 1;
	this->_size = size;
	this->_sign = 0;
	this->_digits = new unsigned int[this->_size]();
}

unsigned int & bigNum::operator[](int i)
{
	if (i < 0)
		return this->_digits[this->_size + i];
	return this->_digits[i];
}

unsigned int bigNum::operator[](int i) const
{
	if (i < 0)
		return this->_digits[this->_size + i];
	return this->_digits[i];
}

void bigNum::_copy(const bigNum &rhv)
{
	this->_size = rhv._size;
	if (!_size)
	{
		this->_digits = new unsigned int[1];
		this->_digits[0] = 0;
		this->_sign = 0;
		return;
	}
	this->_digits = new unsigned int[_size];
	this->_sign = rhv._sign;
	memcpy(_digits, rhv._digits, _size*sizeof(unsigned int));
	return;
}

void bigNum::_DelZeroes()
{
	while ((_size - 1) && _digits && _digits[_size - 1] == 0)
		this->_size--;

	if (this->_size == 1 && _digits[0] == 0)
		this->_sign = 0;
}

long long int bigNum::_compare(const bigNum& B)
{
	int thisSign = 1;
	if(this->_sign == 1)
		thisSign = -1;

	if(this->_sign != B._sign)
		return thisSign;

	if (this->_size > B._size)
		return thisSign;

	if (this->_size < B._size)
		return -thisSign;

	int i = this->_size - 1;

	while( this->_digits[i] == B[i] && i > 0)
	{
		i--;
	}
	return ((long long int) this->_digits[i] - (long long int)B[i])*thisSign;
}

void bigNum::_shiftLeft(int s)
{
  unsigned int* newDig = new unsigned int[this->_size + s]();
	for (int i = 0; i < this->_size; i++)
	{
		if (i + s >= 0)
		{
			newDig[i + s] = this->_digits[i];
		}
	}
	delete[] this->_digits;
	this->_digits = newDig;
	this->_size += s;
	_DelZeroes();
}

bigNum bigNum::_sumAndSub(const bigNum& left, const bigNum& right) const
{
	bigNum A = left, B = right;
	A._sign = 0;
	B._sign = 0;
	if (A > B)
	{
		A._sign = left._sign;
		B._sign = right._sign;
	}
	else
	{
		A = right;
		B = left;
	}

	if (A._sign == B._sign)
	{
		bigNum res;
		res._setSize(A._size + 1);

		unsigned int carry = 0;
		for (int i = 0; i < B._size; i++)
		{
			unsigned int tmp = A[i] + B[i] + carry;
			res[i] = tmp % BASE;
			carry = tmp / BASE;
		}
		for (int i = B._size; i < A._size; i++)
		{
			unsigned int tmp = A[i] + carry;
			res[i] = tmp % BASE;
			carry = tmp / BASE;
		}
		res[A._size] = carry;
		res._sign = A._sign;
		res._DelZeroes();
		return res;
	}
	else
	{
		bigNum res;
		res._setSize(A._size);

		unsigned int carry = 0;
		for (int i = 0; i < B._size; i++)
		{
			int tmp = A[i] - B[i] - carry;
			carry = 0;
			if (tmp < 0)
			{
				carry = 1;
				tmp += BASE;
			}
			res[i] = tmp;
		}

		for (int i = B._size; i < A._size; i++)
		{
			int tmp = A[i] - carry;
			carry = 0;
			if (tmp < 0)
			{
				carry = 1;
				tmp += BASE;
			}
			res[i] = tmp;
		}
		res._sign = A._sign;
		res._DelZeroes();
		return res;
	}
}

bigNum bigNum::_multiplication(const bigNum A, const bigNum B) const
{
	bigNum res;
	res._setSize(A._size + B._size);
	unsigned int carry = 0;
	for (int i = 0; i < B._size; i++)
	{
		carry = 0;
		for (int j = 0; j < A._size; j++)
		{
			unsigned long long int tmp = (unsigned long long int) B[i] * (unsigned long long int) A[j] + carry + (unsigned long long int) res[i + j];
			carry = tmp / BASE;
			res[i + j] = tmp % BASE;
		}
		res[i + A._size] = carry;
	}

	res._sign = (A._sign != B._sign);
	res._DelZeroes();
	return res;
}

bigNum bigNum::_dividing(const bigNum& A, const bigNum& B, bigNum &remainder) const
{
	remainder = A;
	remainder._sign = 0;

	bigNum divider = B;
	divider._sign = 0;

	if (divider == bigNum((long long int) 0))
	{
		throw DIV_BY_ZERO;
	}

	if (remainder < divider)
	{
		remainder = A;
		return bigNum((long long int) 0);
	}

	bigNum res;
	res._setSize(A._size - B._size + 1);

	for (int i = A._size - B._size + 1; i; i--)
	{
		long long int qGuessMax = BASE;
		long long int qGuessMin = 0;
		long long int qGuess = qGuessMax;

		while (qGuessMax - qGuessMin > 1)
		{
			qGuess = (qGuessMax + qGuessMin) / 2;

			bigNum tmp = divider * qGuess;
			tmp._shiftLeft(i - 1);
			if (tmp > remainder)
				qGuessMax = qGuess;
			else
				qGuessMin = qGuess;
		}
		bigNum tmp = divider * qGuessMin;
		tmp._shiftLeft(i - 1);
		remainder = remainder - tmp;
		res[i - 1] = qGuessMin;
	}

	res._sign = (A._sign != B._sign);
	remainder._sign = (A._sign != B._sign);
	remainder._DelZeroes();
	res._DelZeroes();

	return res;
}

bool bigNum::Odd()
{
    if (this->_size == 0)
		return false;

	return (this->_digits[0] & 1);
}

bigNum to_pow(const bigNum& A, const bigNum& B, bigNum& modulus)
{
	if (modulus <= (long long int) 0)
		return A ^ B;

    bigNum a(A % modulus), b(B), result(1);

	while (b != 0)
	{
		if (b.Odd())
			result = (result * a) % modulus;
		a = (a * a) % modulus;
		b = b / 2;
	}

	return result;
}

void go_generate()
{
	srand(time(0));
}

bigNum random_big(bigNum max_value)
{
	bigNum res = 1;
	res._setSize(max_value._size);
	int i = 0;

	while(i != max_value._size-1)
	{
		res._digits[i] = (rand()*30518) % BASE;
		i++;
	}
	res._digits[i] = rand() % max_value._digits[i];
	
	res._DelZeroes();
	return res;
}

bigNum random_fixlen(int len)
{
	bigNum res = 1;
	res._setSize(len / 9);
	int i = 0;

	while(i != (len/9 - 1))
	{
		res._digits[i] = (rand() * 30517) % BASE;
		i++;
	}

	res._digits[i] = (BASE / 10) + (rand() * 27466) % BASE;

	return res;
}

bigNum& bigNum::operator=(const bigNum& rhv)
{
	if (this->_digits == rhv._digits)
		return *this;
	if (this->_size)
		delete[] this->_digits;
	_copy(rhv);
	return *this;
}


bigNum bigNum::operator+(const bigNum& right) const
{
	return _sumAndSub(*this, right);
}

bigNum bigNum::operator-() const
{// унарный минус
	bigNum res = *this;
	res._sign = !res._sign;
	return res;
}

bigNum bigNum::operator-(const bigNum& right) const
{
	return bigNum(*this + (-right));
}

bigNum bigNum::operator*(const bigNum& right) const
{
	return _multiplication(*this, right);
}

bigNum bigNum::operator/(const bigNum& right) const
{
	bigNum rem;
	return _dividing(*this, right, rem);
}

bigNum bigNum::operator%(const bigNum& right) const
{
	bigNum rem;
	_dividing(*this, right, rem);
	return rem;
}

bigNum& bigNum::operator^(const bigNum& right) const
{// возведение *this в степень right
	bigNum* res = new bigNum(1);
	bigNum base = *this;
	for (bigNum i = right; i > (long long int) 0; i = i - 1)
		*res = *res * base;
	return *res;
}



bool bigNum::operator>(const bigNum& B)
{
	return this->_compare(B) > 0;
}

bool bigNum::operator>=(const bigNum& B)
{
	return this->_compare(B) >= 0;
}

bool bigNum::operator<(const bigNum& B)
{
	return this->_compare(B) < 0;
}

bool bigNum::operator<=(const bigNum& B)
{
	return this->_compare(B) <= 0;
}

bool bigNum::operator==(const bigNum& B)
{
	return this->_compare(B) == 0;
}

bool bigNum::operator!=(const bigNum& B)
{
	return this->_compare(B) != 0;
}



std::ostream& operator<<(std::ostream &out, bigNum A)
{
	char* str = A.getString();
	out << str;
	delete[] str;
	return out;
}

std::istream& operator>>(std::istream &is, bigNum &A)
{
	char string[10000];
	is >> string;
	bigNum res(string);
	A = res;
	return is;
}

char* bigNum::__str__()
{
	return getString();
}

char* bigNum::__repr__()
{
	return getString();
}

bigNum bigNum::operator+(const int& right) const
{
	return _sumAndSub(*this, (bigNum)right);
}

bigNum bigNum::operator-(const int& right) const
{
	return *this + (bigNum)(-right);
}

bigNum bigNum::operator*(const int& right) const
{
	return _multiplication(*this, (bigNum)right);
}

bigNum bigNum::operator/(const int& right) const
{
	bigNum rem;
	return _dividing(*this, (bigNum)right, rem);
}

bigNum bigNum::operator%(const int& right) const
{
	bigNum rem;
	_dividing(*this, (bigNum)right, rem);
	return rem;
}

bool bigNum::operator>(const int& B)
{
	return this->_compare((bigNum)B) > 0;
}

bool bigNum::operator>=(const int& B)
{
	return this->_compare((bigNum)B) >= 0;
}

bool bigNum::operator<(const int& B)
{
	return this->_compare((bigNum)B) < 0;
}

bool bigNum::operator<=(const int& B)
{
	return this->_compare((bigNum)B) <= 0;
}

bool bigNum::operator==(const int& B)
{
	return this->_compare((bigNum)B) == 0;
}

bool bigNum::operator!=(const int& B)
{
	return this->_compare((bigNum)B) != 0;
}
