#include "python.h" 

//static PyObject *

static PyObject* spam_ret_service_key(PyObject* self)
{
	const char* str = "TM2mB7BkLj7%2B1mK%2FbNgWbxjMPtdffuyVQbT46zhjwGtnC%2FEA6FQwymPyHVNcFFdJN%2FaQuqSYutGF33dW20COZg%3D%3D";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_google_api_key(PyObject* self)
{
	const char* str = "AIzaSyCCnEO6srD6HY1jEoZqvDfH04T0ihv5uy8";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_passwd(PyObject* self)
{
	const char* str = "ufjw djqt ffsy apln";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_gmail_addr(PyObject* self)
{
	const char* str = "shinmg00@tukorea.ac.kr";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_token(PyObject* self)
{
	const char* str = "7094473827:AAEzKqA5yn83yg8jBo5BFGPyflghBWSlYo4";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyObject* spam_ret_user_id(PyObject* self)
{
	const char* str = "6858392538";

	// Python ���ڿ� ��ü�� ��ȯ�Ͽ� ��ȯ
	return Py_BuildValue("s", str);
}

static PyMethodDef SpamMethods[] = {
	{ "ret_google_api_key", spam_ret_google_api_key, METH_NOARGS, "Return a google API key." },
	{ "ret_service_key", spam_ret_service_key, METH_NOARGS, "Return a service key." },
	{ "ret_gmail_addr", spam_ret_gmail_addr, METH_NOARGS, "Return a gmail address." },
	{ "ret_passwd", spam_ret_passwd, METH_NOARGS, "Return a password." },
	{ "ret_token", spam_ret_token, METH_NOARGS, "Return a token." },
	{ "ret_user_id", spam_ret_user_id, METH_NOARGS, "Return a telegram user id." },
	{ NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef spammodule = {
	PyModuleDef_HEAD_INIT,
	"spam",            // ��� �̸�
	"It is smg module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
	-1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
	return PyModule_Create(&spammodule);
}
