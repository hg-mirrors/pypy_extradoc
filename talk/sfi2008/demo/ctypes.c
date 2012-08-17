static int
KeepRef(CDataObject *target, Py_ssize_t index, PyObject *keep)
{
	int result;
	CDataObject *ob;
	PyObject *key;

/* Optimization: no need to store None */
	if (keep == Py_None) {
		Py_DECREF(Py_None);
		return 0;
	}
	ob = CData_GetContainer(target);
	if (ob->b_objects == NULL || !PyDict_Check(ob->b_objects)) {
		Py_XDECREF(ob->b_objects);
		ob->b_objects = keep; /* refcount consumed */
		return 0;
	}
	key = unique_key(target, index);
	if (key == NULL) {
		Py_DECREF(keep);
		return -1;
	}
	result = PyDict_SetItem(ob->b_objects, key, keep);
	Py_DECREF(key);
	Py_DECREF(keep);
	return result;
}
