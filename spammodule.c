#include "python.h" 

//static PyObject *

static PyObject* spam_ret_service_key(PyObject* self)
{
	const char* str = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_google_api_key(PyObject* self)
{
	const char* str = "AIzaSyCCnEO6srD6HY1jEoZqvDfH04T0ihv5uy8";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_passwd(PyObject* self)
{
	const char* str = "ufjw djqt ffsy apln";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_gmail_addr(PyObject* self)
{
	const char* str = "shinmg00@tukorea.ac.kr";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_token(PyObject* self)
{
	const char* str = "7094473827:AAEzKqA5yn83yg8jBo5BFGPyflghBWSlYo4";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_user_id(PyObject* self)
{
	const char* str = "6858392538";

	// Python 문자열 객체로 변환하여 반환
	return Py_BuildValue("s", str);
}

static PyMethodDef SpamMethods[] = {
	{ "ret_google_api_key", spam_ret_google_api_key, METH_NOARGS, "Return a google API key." },
	{ "ret_service_key", spam_ret_service_key, METH_NOARGS, "Return a service key." },
	{ "ret_gmail_addr", spam_ret_gmail_addr, METH_NOARGS, "Return a gmail address." },
	{ "ret_passwd", spam_ret_passwd, METH_NOARGS, "Return a password." },
	{ "ret_token", spam_ret_token, METH_NOARGS, "Return a token." },
	{ "ret_user_id", spam_ret_user_id, METH_NOARGS, "Return a telegram user id." },
	{ NULL, NULL, 0, NULL } // 배열의 끝을 나타냅니다.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // 모듈 이름
	"It is smg module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
	-1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
