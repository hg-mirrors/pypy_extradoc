/***********************************************************/
/***  Implementations                                    ***/

#define PYPY_NOT_MAIN_FILE
#include "common_header.h"
#include "structdef.h"
#include "forwarddecl.h"

#define HAVE_RTYPER
typedef struct pypy_rpy_string0 RPyString;
typedef struct pypy_list0 RPyListOfString;
typedef struct pypy_tuple2_0 RPyFREXP_RESULT;
typedef struct pypy_tuple2_1 RPyMODF_RESULT;
typedef struct pypy_tuple10_0 RPySTAT_RESULT;
typedef struct pypy_tuple2_2 RPyPIPE_RESULT;
typedef struct pypy_tuple2_2 RPyWAITPID_RESULT;
#define	_RPyListOfString_SetItem	pypy_g__RPyListOfString_SetItem__listPtr_Signed_rpy_str
#define	_RPyListOfString_GetItem	pypy_g__RPyListOfString_GetItem__listPtr_Signed
#define	RPyString_New	pypy_g_RPyString_New__Signed
#define	_RPyListOfString_New	pypy_g__RPyListOfString_New__Signed
#define	_RPyListOfString_Length	pypy_g__RPyListOfString_Length__listPtr
typedef struct pypy_object_vtable0 *RPYTHON_EXCEPTION_VTABLE;
typedef struct pypy_object0 *RPYTHON_EXCEPTION;
#define	RPYTHON_EXCEPTION_MATCH	pypy_g_ll_issubclass__object_vtablePtr_object_vtablePtr
#define	RPYTHON_TYPE_OF_EXC_INST	pypy_g_ll_type__objectPtr
#define	RPYTHON_RAISE_OSERROR	pypy_g_ll_raise_OSError__Signed
#define	_RPyExceptionOccurred	pypy_g__RPyExceptionOccurred
#define	RPyExceptionOccurred1	pypy_g_RPyExceptionOccurred
#define	RPyFetchExceptionType	pypy_g_RPyFetchExceptionType
#define	RPyFetchExceptionValue	pypy_g_RPyFetchExceptionValue
#define	RPyClearException	pypy_g_RPyClearException
#define	RPyRaiseException	pypy_g_RPyRaiseException
#define	RPyExc_KeyError	(&pypy_g_exceptions_KeyError.ke_super.le_super.se_super.e_super)
#define	RPyExc_RuntimeError	(&pypy_g_exceptions_RuntimeError.re_super.se_super.e_super)
#define	RPyExc_MemoryError	(&pypy_g_exceptions_MemoryError.me_super.se_super.e_super)
#define	RPyExc_ZeroDivisionError	(&pypy_g_exceptions_ZeroDivisionError.zde_super.ae_super.se_super.e_super)
#define	RPyExc_IOError	(&pypy_g_exceptions_IOError.ioe_super.ee_super.se_super.e_super)
#define	RPyExc_StopIteration	(&pypy_g_exceptions_StopIteration.si_super.e_super)
#define	RPyExc_OverflowError	(&pypy_g_exceptions_OverflowError.oe_super.ae_super.se_super.e_super)
#define	RPyExc_TypeError	(&pypy_g_exceptions_TypeError.te_super.se_super.e_super)
#define	RPyExc_OSError	(&pypy_g_exceptions_EnvironmentError.ee_super.se_super.e_super)
#define	RPyExc_thread_error	(&pypy_g_object)
#define	RPyExc_AssertionError	(&pypy_g_exceptions_AssertionError.ae_super.se_super.e_super)
#define	RPyExc_ValueError	(&pypy_g_exceptions_ValueError.ve_super.se_super.e_super)
#define	RPyExc_IndexError	(&pypy_g_exceptions_IndexError.ie_super.le_super.se_super.e_super)

#include "src/g_include.h"

/*/*/
long pypy_g_entry_point(struct pypy_list0 *l_argv_0) {
	bool_t l_v12; bool_t l_v17; bool_t l_v20; bool_t l_v26; bool_t l_v28;
	bool_t l_v30; bool_t l_v33; bool_t l_v36; bool_t l_v39; bool_t l_v42;
	bool_t l_v5; bool_t l_v9; long l_v0; long l_v11; long l_v16;
	long l_v19; long l_v2; long l_v43; long l_v4; long l_v8;
	struct pypy_array0 *l_v14; struct pypy_array0 *l_v22;
	struct pypy_object_vtable0 *l_v25; struct pypy_object_vtable0 *l_v27;
	struct pypy_object_vtable0 *l_v29; struct pypy_object_vtable0 *l_v32;
	struct pypy_object_vtable0 *l_v35; struct pypy_object_vtable0 *l_v38;
	struct pypy_object_vtable0 *l_v41; struct pypy_rpy_string0 *l_v1;
	struct pypy_rpy_string0 *l_v23; struct pypy_rpy_string0 *l_v3;

    block0:
	l_v4 = l_argv_0->l_length;
	OP_INT_NE(l_v4, 3L, l_v5);
	/* kept alive: l_argv_0 */ ;
	if (l_v5) {
		goto block7;
	}
	goto block1;

    block1:
	RPyAssert(1, "unexpectedly negative list getitem index");
	l_v8 = l_argv_0->l_length;
	OP_INT_LT(1L, l_v8, l_v9);
	RPyAssert(l_v9, "list getitem index out of bound");
	l_v11 = l_argv_0->l_length;
	OP_INT_LT(1L, l_v11, l_v12);
	RPyAssert(l_v12, "getitem out of bounds");
	l_v14 = l_argv_0->l_items;
	l_v3 = l_v14->items[1L];
	RPyAssert(1, "unexpectedly negative list getitem index");
	l_v16 = l_argv_0->l_length;
	OP_INT_LT(2L, l_v16, l_v17);
	RPyAssert(l_v17, "list getitem index out of bound");
	l_v19 = l_argv_0->l_length;
	OP_INT_LT(2L, l_v19, l_v20);
	RPyAssert(l_v20, "getitem out of bounds");
	l_v22 = l_argv_0->l_items;
	l_v23 = l_v22->items[2L];
	/* kept alive: l_argv_0 */ ;
	l_v2 = pypy_g_ll_int__rpy_stringPtr_Signed(l_v23, 10L);
	l_v25 = (&pypy_g_ExcData)->ed_exc_type;
	l_v26 = (l_v25 == NULL);
	if (!l_v26) {
		l_v43 = -1L;
		goto block6;
	}
	goto block2;

    block2:
	l_v0 = pypy_g_interpret(l_v3, l_v2);
	l_v27 = (&pypy_g_ExcData)->ed_exc_type;
	l_v28 = (l_v27 == NULL);
	if (!l_v28) {
		l_v43 = -1L;
		goto block6;
	}
	goto block3;

    block3:
	l_v1 = pypy_g_ll_int2dec__Signed(l_v0);
	l_v29 = (&pypy_g_ExcData)->ed_exc_type;
	l_v30 = (l_v29 == NULL);
	if (!l_v30) {
		l_v43 = -1L;
		goto block6;
	}
	goto block4;

    block4:
	pypy_g_rpython_print_item(l_v1);
	l_v32 = (&pypy_g_ExcData)->ed_exc_type;
	l_v33 = (l_v32 == NULL);
	if (!l_v33) {
		l_v43 = -1L;
		goto block6;
	}
	goto block5;

    block5:
	pypy_g_rpython_print_newline();
	l_v35 = (&pypy_g_ExcData)->ed_exc_type;
	l_v36 = (l_v35 == NULL);
	if (!l_v36) {
		l_v43 = -1L;
		goto block6;
	}
	l_v43 = 0L;
	goto block6;

    block6:
	RPY_DEBUG_RETURN();
	return l_v43;

    block7:
	pypy_g_rpython_print_item(((struct pypy_rpy_string0 *)(void*)(&pypy_g_rpy_string)));
	l_v38 = (&pypy_g_ExcData)->ed_exc_type;
	l_v39 = (l_v38 == NULL);
	if (!l_v39) {
		l_v43 = -1L;
		goto block6;
	}
	goto block8;

    block8:
	pypy_g_rpython_print_newline();
	l_v41 = (&pypy_g_ExcData)->ed_exc_type;
	l_v42 = (l_v41 == NULL);
	if (!l_v42) {
		l_v43 = -1L;
		goto block6;
	}
	l_v43 = 2L;
	goto block6;
}
/*/*/
void pypy_g__RPyListOfString_SetItem__listPtr_Signed_rpy_str(struct pypy_list0 *l_l_0, long l_index_0, struct pypy_rpy_string0 *l_newstring_0) {

    block0:
	pypy_g_ll_setitem_nonneg__dum_nocheckConst_listPtr_Sign(l_l_0, l_index_0, l_newstring_0);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return /* nothing */;
}
/*/*/
struct pypy_rpy_string0 *pypy_g__RPyListOfString_GetItem__listPtr_Signed(struct pypy_list0 *l_l_1, long l_index_1) {
	struct pypy_rpy_string0 *l_v46;

    block0:
	l_v46 = pypy_g_ll_getitem_fast__listPtr_Signed(l_l_1, l_index_1);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v46;
}
/*/*/
struct pypy_rpy_string0 *pypy_g_RPyString_New__Signed(long l_length_0) {
	struct pypy_rpy_string0 *l_v47;

    block0:
	l_v47 = pypy_g_mallocstr__Signed(l_length_0);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v47;
}
/*/*/
struct pypy_list0 *pypy_g__RPyListOfString_New__Signed(long l_length_1) {
	struct pypy_list0 *l_v48;

    block0:
	l_v48 = pypy_g_ll_newlist__GcStruct_listLlT_Signed(l_length_1);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v48;
}
/*/*/
long pypy_g__RPyListOfString_Length__listPtr(struct pypy_list0 *l_l_2) {
	long l_v49;

    block0:
	l_v49 = pypy_g_ll_length__listPtr(l_l_2);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v49;
}
/*/*/
bool_t pypy_g_ll_issubclass__object_vtablePtr_object_vtablePtr(struct pypy_object_vtable0 *l_subcls_0, struct pypy_object_vtable0 *l_cls_0) {
	bool_t l_v52; bool_t l_v54; bool_t l_v55; long l_v50; long l_v51;
	long l_v53;

    block0:
	l_v51 = l_cls_0->ov_subclassrange_min;
	l_v50 = l_subcls_0->ov_subclassrange_min;
	OP_INT_LE(l_v51, l_v50, l_v52);
	if (l_v52) {
		goto block2;
	}
	l_v55 = l_v52;
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v55;

    block2:
	l_v53 = l_cls_0->ov_subclassrange_max;
	OP_INT_LE(l_v50, l_v53, l_v54);
	l_v55 = l_v54;
	goto block1;
}
/*/*/
struct pypy_object_vtable0 *pypy_g_ll_type__objectPtr(struct pypy_object0 *l_obj_0) {
	struct pypy_object0 *l_v57; struct pypy_object_vtable0 *l_v56;

    block0:
	l_v57 = (struct pypy_object0 *)l_obj_0;
	l_v56 = l_v57->o_typeptr;
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v56;
}
/*/*/
void pypy_g_ll_raise_OSError__Signed(long l_errno_0) {
	bool_t l_v60; struct pypy_exceptions_OSError0 *l_v58;
	struct pypy_object0 *l_v61; struct pypy_object_vtable0 *l_v64;
	void* l_v59;

    block0:
	l_v59 = pypy_g_ll_malloc_fixedsize_atomic__Signed_funcPtr((sizeof(struct pypy_exceptions_OSError0) * 1), ((void (*)(void*)) NULL));
	l_v58 = (struct pypy_exceptions_OSError0 *)l_v59;
	l_v60 = (l_v58 != NULL);
	if (!l_v60) {
		goto block2;
	}
	goto block1;

    block1:
	l_v61 = (struct pypy_object0 *)l_v58;
	l_v61->o_typeptr = (&pypy_g_exceptions_OSError_vtable.ose_super.ee_super.se_super.e_super);
	l_v58->ose_inst_errno = l_errno_0;
	l_v64 = l_v61->o_typeptr;
	pypy_g_RPyRaiseException(l_v64, l_v61);
	goto block2;

    block2:
	RPY_DEBUG_RETURN();
	return /* nothing */;
}
/*/*/
long pypy_g__RPyExceptionOccurred(void) {
	bool_t l_v69; long l_v67; struct pypy_object_vtable0 *l_v68;

    block0:
	l_v68 = (&pypy_g_ExcData)->ed_exc_type;
	l_v69 = (l_v68 != NULL);
	OP_CAST_BOOL_TO_INT(l_v69, l_v67);
	goto block1;

    block1:
	return l_v67;
}
/*/*/
bool_t pypy_g_RPyExceptionOccurred(void) {
	bool_t l_v70; struct pypy_object_vtable0 *l_v71;

    block0:
	l_v71 = (&pypy_g_ExcData)->ed_exc_type;
	l_v70 = (l_v71 != NULL);
	goto block1;

    block1:
	return l_v70;
}
/*/*/
struct pypy_object_vtable0 *pypy_g_RPyFetchExceptionType(void) {
	struct pypy_object_vtable0 *l_v72;

    block0:
	l_v72 = (&pypy_g_ExcData)->ed_exc_type;
	goto block1;

    block1:
	return l_v72;
}
/*/*/
struct pypy_object0 *pypy_g_RPyFetchExceptionValue(void) {
	struct pypy_object0 *l_v73;

    block0:
	l_v73 = (&pypy_g_ExcData)->ed_exc_value;
	goto block1;

    block1:
	return l_v73;
}
/*/*/
void pypy_g_RPyClearException(void) {

    block0:
	(&pypy_g_ExcData)->ed_exc_type = ((struct pypy_object_vtable0 *) NULL);
	(&pypy_g_ExcData)->ed_exc_value = ((struct pypy_object0 *) NULL);
	goto block1;

    block1:
	return /* nothing */;
}
/*/*/
void pypy_g_RPyRaiseException(struct pypy_object_vtable0 *l_etype_0, struct pypy_object0 *l_evalue_0) {

    block0:
	(&pypy_g_ExcData)->ed_exc_type = l_etype_0;
	(&pypy_g_ExcData)->ed_exc_value = l_evalue_0;
	goto block1;

    block1:
	return /* nothing */;
}
/*/*/
long pypy_g_ll_int__rpy_stringPtr_Signed(struct pypy_rpy_string0 *l_s_2, long l_base_1) {
	long l_c_0; struct pypy_array1 *l_chars_0; long l_digit_0;
	struct pypy_object_vtable0 *l_etype_1;
	struct pypy_object0 *l_evalue_1; long l_i_1; long l_i_2; long l_i_3;
	long l_oldpos_0; long l_sign_0; long l_strlen_0; bool_t l_v100;
	bool_t l_v101; bool_t l_v102; bool_t l_v104; bool_t l_v108;
	bool_t l_v111; bool_t l_v115; bool_t l_v120; bool_t l_v80;
	bool_t l_v82; bool_t l_v83; bool_t l_v84; bool_t l_v86; bool_t l_v88;
	bool_t l_v89; bool_t l_v90; bool_t l_v91; bool_t l_v92; bool_t l_v93;
	bool_t l_v96; bool_t l_v99; char l_v114; char l_v119; char l_v85;
	char l_v87; char l_v95; char l_v98; long l_v103; long l_v105;
	long l_v106; long l_v107; long l_v109; long l_v110; long l_v112;
	long l_v113; long l_v116; long l_v117; long l_v118; long l_v121;
	long l_v122; long l_v94; long l_v97; long l_val_0;

    block0:
	OP_INT_LE(2L, l_base_1, l_v80);
	if (l_v80) {
		goto block3;
	}
	l_etype_1 = (&pypy_g_exceptions_ValueError_vtable.ve_super.se_super.e_super);
	l_evalue_1 = (&pypy_g_exceptions_ValueError.ve_super.se_super.e_super);
	goto block1;

    block1:
	pypy_g_RPyRaiseException(l_etype_1, l_evalue_1);
	l_v122 = -1L;
	goto block2;

    block2:
	RPY_DEBUG_RETURN();
	return l_v122;

    block3:
	OP_INT_LE(l_base_1, 36L, l_v82);
	if (l_v82) {
		goto block4;
	}
	l_etype_1 = (&pypy_g_exceptions_ValueError_vtable.ve_super.se_super.e_super);
	l_evalue_1 = (&pypy_g_exceptions_ValueError.ve_super.se_super.e_super);
	goto block1;

    block4:
	l_chars_0 = &l_s_2->rs_chars;
	l_strlen_0 = l_chars_0->length;
	l_i_1 = 0L;
	goto block5;

    block5:
	OP_INT_LT(l_i_1, l_strlen_0, l_v83);
	if (l_v83) {
		goto block32;
	}
	goto block6;

    block6:
	OP_INT_LT(l_i_1, l_strlen_0, l_v84);
	if (l_v84) {
		goto block7;
	}
	l_etype_1 = (&pypy_g_exceptions_ValueError_vtable.ve_super.se_super.e_super);
	l_evalue_1 = (&pypy_g_exceptions_ValueError.ve_super.se_super.e_super);
	goto block1;

    block7:
	l_v85 = l_chars_0->items[l_i_1];
	OP_CHAR_EQ(l_v85, '-', l_v86);
	if (l_v86) {
		goto block31;
	}
	goto block8;

    block8:
	l_v87 = l_chars_0->items[l_i_1];
	OP_CHAR_EQ(l_v87, '+', l_v88);
	if (l_v88) {
		goto block30;
	}
	l_sign_0 = 1L;
	l_oldpos_0 = l_i_1;
	goto block9;

    block9:
	OP_INT_LT(l_oldpos_0, l_strlen_0, l_v89);
	if (l_v89) {
		goto block28;
	}
	l_val_0 = 0L;
	l_i_2 = l_oldpos_0;
	goto block10;

    block10:
	OP_INT_LT(l_i_2, l_strlen_0, l_v90);
	if (l_v90) {
		goto block17;
	}
	goto block11;

    block11:
	OP_INT_EQ(l_i_2, l_oldpos_0, l_v91);
	if (l_v91) {
		l_etype_1 = (&pypy_g_exceptions_ValueError_vtable.ve_super.se_super.e_super);
		l_evalue_1 = (&pypy_g_exceptions_ValueError.ve_super.se_super.e_super);
		goto block1;
	}
	l_i_3 = l_i_2;
	goto block12;

    block12:
	OP_INT_LT(l_i_3, l_strlen_0, l_v92);
	if (l_v92) {
		goto block15;
	}
	goto block13;

    block13:
	OP_INT_EQ(l_i_3, l_strlen_0, l_v93);
	if (l_v93) {
		goto block14;
	}
	l_etype_1 = (&pypy_g_exceptions_ValueError_vtable.ve_super.se_super.e_super);
	l_evalue_1 = (&pypy_g_exceptions_ValueError.ve_super.se_super.e_super);
	goto block1;

    block14:
	OP_INT_MUL(l_sign_0, l_val_0, l_v94);
	l_v122 = l_v94;
	goto block2;

    block15:
	l_v95 = l_chars_0->items[l_i_3];
	OP_CHAR_EQ(l_v95, ' ', l_v96);
	if (l_v96) {
		goto block16;
	}
	goto block13;

    block16:
	OP_INT_ADD(l_i_3, 1L, l_v97);
	l_i_3 = l_v97;
	goto block12;

    block17:
	l_v98 = l_chars_0->items[l_i_2];
	OP_CAST_CHAR_TO_INT(l_v98, l_c_0);
	OP_INT_LE(97L, l_c_0, l_v99);
	if (l_v99) {
		goto block26;
	}
	goto block18;

    block18:
	OP_INT_LE(65L, l_c_0, l_v100);
	if (l_v100) {
		goto block24;
	}
	goto block19;

    block19:
	OP_INT_LE(48L, l_c_0, l_v101);
	if (l_v101) {
		goto block20;
	}
	goto block11;

    block20:
	OP_INT_LE(l_c_0, 57L, l_v102);
	if (l_v102) {
		goto block21;
	}
	goto block11;

    block21:
	OP_INT_SUB(l_c_0, 48L, l_v103);
	l_digit_0 = l_v103;
	goto block22;

    block22:
	OP_INT_GE(l_digit_0, l_base_1, l_v104);
	if (l_v104) {
		goto block11;
	}
	goto block23;

    block23:
	OP_INT_MUL(l_val_0, l_base_1, l_v105);
	OP_INT_ADD(l_v105, l_digit_0, l_v106);
	OP_INT_ADD(l_i_2, 1L, l_v107);
	l_val_0 = l_v106;
	l_i_2 = l_v107;
	goto block10;

    block24:
	OP_INT_LE(l_c_0, 90L, l_v108);
	if (l_v108) {
		goto block25;
	}
	goto block19;

    block25:
	OP_INT_SUB(l_c_0, 65L, l_v109);
	OP_INT_ADD(l_v109, 10L, l_v110);
	l_digit_0 = l_v110;
	goto block22;

    block26:
	OP_INT_LE(l_c_0, 122L, l_v111);
	if (l_v111) {
		goto block27;
	}
	goto block18;

    block27:
	OP_INT_SUB(l_c_0, 97L, l_v112);
	OP_INT_ADD(l_v112, 10L, l_v113);
	l_digit_0 = l_v113;
	goto block22;

    block28:
	l_v114 = l_chars_0->items[l_oldpos_0];
	OP_CHAR_EQ(l_v114, ' ', l_v115);
	if (l_v115) {
		goto block29;
	}
	l_val_0 = 0L;
	l_i_2 = l_oldpos_0;
	goto block10;

    block29:
	OP_INT_ADD(l_oldpos_0, 1L, l_v116);
	l_oldpos_0 = l_v116;
	goto block9;

    block30:
	OP_INT_ADD(l_i_1, 1L, l_v117);
	l_sign_0 = 1L;
	l_oldpos_0 = l_v117;
	goto block9;

    block31:
	OP_INT_ADD(l_i_1, 1L, l_v118);
	l_sign_0 = -1L;
	l_oldpos_0 = l_v118;
	goto block9;

    block32:
	l_v119 = l_chars_0->items[l_i_1];
	OP_CHAR_EQ(l_v119, ' ', l_v120);
	if (l_v120) {
		goto block33;
	}
	goto block6;

    block33:
	OP_INT_ADD(l_i_1, 1L, l_v121);
	l_i_1 = l_v121;
	goto block5;
}
/*/*/
long pypy_g_interpret(struct pypy_rpy_string0 *l_v123, long l_arg_0) {
	char l_c_1; struct pypy_rpn_State0 *l_state_0; bool_t l_v137;
	bool_t l_v142; bool_t l_v145; bool_t l_v152; bool_t l_v155;
	bool_t l_v157; bool_t l_v165; bool_t l_v167; bool_t l_v169;
	bool_t l_v172; bool_t l_v173; bool_t l_v177; bool_t l_v181;
	bool_t l_v183; bool_t l_v194; bool_t l_v196; bool_t l_v199;
	long l_v124; long l_v126; long l_v129; long l_v130; long l_v131;
	long l_v132; long l_v133; long l_v151; long l_v156; long l_v164;
	long l_v174; long l_v176; long l_v182; long l_v191; long l_v193;
	long l_v198; long l_v202; long l_v206; struct pypy_array1 *l_v127;
	struct pypy_array3 *l_v135; struct pypy_array3 *l_v150;
	struct pypy_array3 *l_v159; struct pypy_array3 *l_v175;
	struct pypy_array3 *l_v185; struct pypy_array3 *l_v201;
	struct pypy_list1 *l_v125; struct pypy_list1 *l_v128;
	struct pypy_list1 *l_v134; struct pypy_list1 *l_v190;
	struct pypy_object0 *l_v138; struct pypy_object_vtable0 *l_v154;
	struct pypy_object_vtable0 *l_v171;
	struct pypy_object_vtable0 *l_v180; void* l_v136; void* l_v141;
	void* l_v144;

    block0:
	l_v136 = pypy_g_ll_malloc_fixedsize__Signed_funcPtr((sizeof(struct pypy_rpn_State0) * 1), ((void (*)(void*)) NULL));
	l_state_0 = (struct pypy_rpn_State0 *)l_v136;
	l_v137 = (l_state_0 != NULL);
	if (!l_v137) {
		l_v206 = -1L;
		goto block10;
	}
	goto block1;

    block1:
	l_v138 = (struct pypy_object0 *)l_state_0;
	l_v138->o_typeptr = (&pypy_g_rpn_State_vtable.s_super);
	RPyAssert(1, "negative list length");
	l_v141 = pypy_g_ll_malloc_fixedsize__Signed_funcPtr((sizeof(struct pypy_list1) * 1), ((void (*)(void*)) NULL));
	l_v134 = (struct pypy_list1 *)l_v141;
	l_v142 = (l_v134 != NULL);
	if (!l_v142) {
		l_v206 = -1L;
		goto block10;
	}
	goto block2;

    block2:
	l_v134->l_length = 0L;
	l_v144 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(0L, (offsetof(struct pypy_array3, items) + (sizeof(long) * 0)), (sizeof(long) * 1), offsetof(struct pypy_array3, length));
	l_v135 = (struct pypy_array3 *)l_v144;
	l_v145 = (l_v135 != NULL);
	if (!l_v145) {
		l_v206 = -1L;
		goto block10;
	}
	goto block3;

    block3:
	l_v134->l_items = l_v135;
	l_state_0->s_inst_stack = l_v134;
	/* kept alive: l_state_0 */ ;
	l_v125 = l_state_0->s_inst_stack;
	l_v131 = l_v125->l_length;
	/* kept alive: l_v125 */ ;
	OP_INT_ADD(l_v131, 1L, l_v132);
	l_v150 = l_v125->l_items;
	l_v151 = l_v150->length;
	OP_INT_GE(l_v151, l_v132, l_v152);
	if (l_v152) {
		goto block17;
	}
	goto block4;

    block4:
	pypy_g__ll_list_resize_really__listPtr_Signed(l_v125, l_v132);
	l_v154 = (&pypy_g_ExcData)->ed_exc_type;
	l_v155 = (l_v154 == NULL);
	if (!l_v155) {
		l_v206 = -1L;
		goto block10;
	}
	goto block5;

    block5:
	l_v156 = l_v125->l_length;
	OP_INT_LT(l_v131, l_v156, l_v157);
	RPyAssert(l_v157, "setitem out of bounds");
	l_v159 = l_v125->l_items;
	l_v159->items[l_v131] = l_arg_0;
	/* kept alive: l_v125 */ ;
	/* kept alive: l_state_0 */ ;
	/* kept alive: l_v123 */ ;
	l_v133 = 0L;
	goto block6;

    block6:
	l_v127 = &l_v123->rs_chars;
	l_v164 = l_v127->length;
	OP_INT_GE(l_v133, l_v164, l_v165);
	/* kept alive: l_v123 */ ;
	if (l_v165) {
		goto block16;
	}
	goto block7;

    block7:
	OP_INT_ADD(l_v133, 1L, l_v129);
	l_c_1 = l_v127->items[l_v133];
	OP_CHAR_LE('0', l_c_1, l_v167);
	/* kept alive: l_v123 */ ;
	if (l_v167) {
		goto block11;
	}
	goto block8;

    block8:
	OP_CHAR_EQ(l_c_1, '+', l_v169);
	if (l_v169) {
		goto block9;
	}
	l_v133 = l_v129;
	goto block6;

    block9:
	pypy_g_State_add(l_state_0);
	l_v171 = (&pypy_g_ExcData)->ed_exc_type;
	l_v172 = (l_v171 == NULL);
	if (!l_v172) {
		l_v206 = -1L;
		goto block10;
	}
	l_v133 = l_v129;
	goto block6;

    block10:
	RPY_DEBUG_RETURN();
	return l_v206;

    block11:
	OP_CHAR_LE(l_c_1, '9', l_v173);
	if (l_v173) {
		goto block12;
	}
	goto block8;

    block12:
	OP_CAST_CHAR_TO_INT(l_c_1, l_v174);
	OP_INT_SUB(l_v174, 48L, l_v124);
	l_v128 = l_state_0->s_inst_stack;
	l_v126 = l_v128->l_length;
	OP_INT_ADD(l_v126, 1L, l_v130);
	l_v175 = l_v128->l_items;
	l_v176 = l_v175->length;
	OP_INT_GE(l_v176, l_v130, l_v177);
	/* kept alive: l_v128 */ ;
	if (l_v177) {
		goto block15;
	}
	goto block13;

    block13:
	pypy_g__ll_list_resize_really__listPtr_Signed(l_v128, l_v130);
	l_v180 = (&pypy_g_ExcData)->ed_exc_type;
	l_v181 = (l_v180 == NULL);
	if (!l_v181) {
		l_v206 = -1L;
		goto block10;
	}
	goto block14;

    block14:
	l_v182 = l_v128->l_length;
	OP_INT_LT(l_v126, l_v182, l_v183);
	RPyAssert(l_v183, "setitem out of bounds");
	l_v185 = l_v128->l_items;
	l_v185->items[l_v126] = l_v124;
	/* kept alive: l_v128 */ ;
	/* kept alive: l_state_0 */ ;
	l_v133 = l_v129;
	goto block6;

    block15:
	l_v128->l_length = l_v130;
	goto block14;

    block16:
	l_v190 = l_state_0->s_inst_stack;
	l_v191 = l_v190->l_length;
	/* kept alive: l_v123 */ ;
	OP_INT_ADD(-1L, l_v191, l_v193);
	OP_INT_GE(l_v193, 0L, l_v194);
	RPyAssert(l_v194, "negative list getitem index out of bound");
	OP_INT_LT(l_v193, l_v191, l_v196);
	RPyAssert(l_v196, "list getitem index out of bound");
	l_v198 = l_v190->l_length;
	OP_INT_LT(l_v193, l_v198, l_v199);
	RPyAssert(l_v199, "getitem out of bounds");
	l_v201 = l_v190->l_items;
	l_v202 = l_v201->items[l_v193];
	/* kept alive: l_v190 */ ;
	/* kept alive: l_state_0 */ ;
	l_v206 = l_v202;
	goto block10;

    block17:
	l_v125->l_length = l_v132;
	goto block5;
}
/*/*/
struct pypy_rpy_string0 *pypy_g_ll_int2dec__Signed(long l_i_0) {
	unsigned long l_i_4; unsigned long l_i_5; long l_j_0; long l_len_0;
	long l_sign_1; bool_t l_v211; bool_t l_v212; bool_t l_v214;
	bool_t l_v215; bool_t l_v216; bool_t l_v219; bool_t l_v220;
	bool_t l_v223; bool_t l_v224; char l_v227; char l_v236; long l_v209;
	long l_v225; long l_v226; long l_v230; long l_v235; long l_v239;
	long l_v241; long l_v244; struct pypy_array1 *l_v228;
	struct pypy_array1 *l_v231; struct pypy_array4 *l_v207;
	struct pypy_rpy_string0 *l_v208; struct pypy_rpy_string0 *l_v243;
	unsigned long l_v213; unsigned long l_v233; unsigned long l_v234;
	unsigned long l_v238; unsigned long l_v242; void* l_v210;
	void* l_v218;

    block0:
	l_v210 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(20L, (offsetof(struct pypy_array4, items) + (sizeof(char) * 0)), (sizeof(char) * 1), offsetof(struct pypy_array4, length));
	l_v207 = (struct pypy_array4 *)l_v210;
	l_v211 = (l_v207 != NULL);
	if (!l_v211) {
		l_v243 = ((struct pypy_rpy_string0 *) NULL);
		goto block10;
	}
	goto block1;

    block1:
	OP_INT_LT(l_i_0, 0L, l_v212);
	if (l_v212) {
		goto block15;
	}
	goto block2;

    block2:
	OP_CAST_INT_TO_UINT(l_i_0, l_v213);
	l_sign_1 = 0L;
	l_i_5 = l_v213;
	goto block3;

    block3:
	OP_UINT_EQ(l_i_5, 0UL, l_v214);
	if (l_v214) {
		goto block14;
	}
	l_len_0 = 0L;
	l_i_4 = l_i_5;
	goto block4;

    block4:
	OP_UINT_IS_TRUE(l_i_4, l_v215);
	if (l_v215) {
		goto block13;
	}
	l_v244 = l_len_0;
	goto block5;

    block5:
	OP_INT_ADD(l_v244, l_sign_1, l_v209);
	OP_INT_GE(l_v209, 0L, l_v216);
	RPyAssert(l_v216, "negative string length");
	l_v218 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_v209, (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, items) + (sizeof(char) * 1)), (sizeof(char) * 1), (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, length)));
	l_v208 = (struct pypy_rpy_string0 *)l_v218;
	l_v219 = (l_v208 != NULL);
	if (!l_v219) {
		l_v243 = ((struct pypy_rpy_string0 *) NULL);
		goto block10;
	}
	goto block6;

    block6:
	OP_INT_IS_TRUE(MALLOC_ZERO_FILLED, l_v220);
	if (l_v220) {
		goto block8;
	}
	goto block7;

    block7:
	l_v208->rs_hash = 0L;
	goto block8;

    block8:
	l_v208->rs_hash = 0L;
	OP_INT_IS_TRUE(l_sign_1, l_v223);
	if (l_v223) {
		goto block12;
	}
	l_j_0 = 0L;
	goto block9;

    block9:
	OP_INT_LT(l_j_0, l_v209, l_v224);
	if (l_v224) {
		goto block11;
	}
	l_v243 = l_v208;
	goto block10;

    block10:
	RPY_DEBUG_RETURN();
	return l_v243;

    block11:
	OP_INT_SUB(l_v209, l_j_0, l_v225);
	OP_INT_SUB(l_v225, 1L, l_v226);
	l_v227 = l_v207->items[l_v226];
	l_v228 = &l_v208->rs_chars;
	l_v228->items[l_j_0] = l_v227;
	OP_INT_ADD(l_j_0, 1L, l_v230);
	l_j_0 = l_v230;
	goto block9;

    block12:
	l_v231 = &l_v208->rs_chars;
	l_v231->items[0L] = '-';
	l_j_0 = 1L;
	goto block9;

    block13:
	OP_UINT_MOD(l_i_4, 10UL, l_v233);
	OP_UINT_ADD(l_v233, 48UL, l_v234);
	OP_CAST_UINT_TO_INT(l_v234, l_v235);
	OP_CAST_INT_TO_CHAR(l_v235, l_v236);
	l_v207->items[l_len_0] = l_v236;
	OP_UINT_FLOORDIV(l_i_4, 10UL, l_v238);
	OP_INT_ADD(l_len_0, 1L, l_v239);
	l_len_0 = l_v239;
	l_i_4 = l_v238;
	goto block4;

    block14:
	l_v207->items[0L] = '0';
	l_v244 = 1L;
	goto block5;

    block15:
	OP_INT_NEG(l_i_0, l_v241);
	OP_CAST_INT_TO_UINT(l_v241, l_v242);
	l_sign_1 = 1L;
	l_i_5 = l_v242;
	goto block3;
}
/*/*/
void pypy_g_rpython_print_item(struct pypy_rpy_string0 *l_v247) {
	bool_t l_v256; bool_t l_v260; bool_t l_v265; bool_t l_v267;
	bool_t l_v275; bool_t l_v280; bool_t l_v282; char l_v245;
	long l_v246; long l_v248; long l_v249; long l_v251; long l_v252;
	long l_v253; long l_v255; long l_v259; long l_v266; long l_v274;
	long l_v281; struct pypy_array1 *l_v250; struct pypy_array5 *l_v258;
	struct pypy_array5 *l_v269; struct pypy_array5 *l_v273;
	struct pypy_array5 *l_v284; struct pypy_object_vtable0 *l_v264;
	struct pypy_object_vtable0 *l_v279;

    block0:
	/* kept alive: l_v247 */ ;
	l_v251 = 0L;
	goto block1;

    block1:
	l_v250 = &l_v247->rs_chars;
	l_v255 = l_v250->length;
	OP_INT_GE(l_v251, l_v255, l_v256);
	/* kept alive: l_v247 */ ;
	if (l_v256) {
		goto block7;
	}
	goto block2;

    block2:
	OP_INT_ADD(l_v251, 1L, l_v246);
	l_v245 = l_v250->items[l_v251];
	l_v248 = (&pypy_g_list)->l_length;
	OP_INT_ADD(l_v248, 1L, l_v252);
	l_v258 = (&pypy_g_list)->l_items;
	l_v259 = l_v258->length;
	OP_INT_GE(l_v259, l_v252, l_v260);
	/* kept alive: l_v247 */ ;
	/* kept alive: (&pypy_g_list) */ ;
	if (l_v260) {
		goto block6;
	}
	goto block3;

    block3:
	pypy_g__ll_list_resize_really__listPtr_Signed_1((&pypy_g_list), l_v252);
	l_v264 = (&pypy_g_ExcData)->ed_exc_type;
	l_v265 = (l_v264 == NULL);
	if (!l_v265) {
		goto block5;
	}
	goto block4;

    block4:
	l_v266 = (&pypy_g_list)->l_length;
	OP_INT_LT(l_v248, l_v266, l_v267);
	RPyAssert(l_v267, "setitem out of bounds");
	l_v269 = (&pypy_g_list)->l_items;
	l_v269->items[l_v248] = l_v245;
	/* kept alive: (&pypy_g_list) */ ;
	l_v251 = l_v246;
	goto block1;

    block5:
	RPY_DEBUG_RETURN();
	return /* nothing */;

    block6:
	(&pypy_g_list)->l_length = l_v252;
	goto block4;

    block7:
	l_v249 = (&pypy_g_list)->l_length;
	OP_INT_ADD(l_v249, 1L, l_v253);
	l_v273 = (&pypy_g_list)->l_items;
	l_v274 = l_v273->length;
	OP_INT_GE(l_v274, l_v253, l_v275);
	/* kept alive: l_v247 */ ;
	/* kept alive: (&pypy_g_list) */ ;
	if (l_v275) {
		goto block10;
	}
	goto block8;

    block8:
	pypy_g__ll_list_resize_really__listPtr_Signed_1((&pypy_g_list), l_v253);
	l_v279 = (&pypy_g_ExcData)->ed_exc_type;
	l_v280 = (l_v279 == NULL);
	if (!l_v280) {
		goto block5;
	}
	goto block9;

    block9:
	l_v281 = (&pypy_g_list)->l_length;
	OP_INT_LT(l_v249, l_v281, l_v282);
	RPyAssert(l_v282, "setitem out of bounds");
	l_v284 = (&pypy_g_list)->l_items;
	l_v284->items[l_v249] = ' ';
	/* kept alive: (&pypy_g_list) */ ;
	goto block5;

    block10:
	(&pypy_g_list)->l_length = l_v253;
	goto block9;
}
/*/*/
void pypy_g_rpython_print_newline(void) {
	long l_i_6; struct pypy_array1 *l_res_chars_0; bool_t l_v293;
	bool_t l_v297; bool_t l_v299; bool_t l_v302; bool_t l_v307;
	bool_t l_v310; bool_t l_v311; bool_t l_v313; bool_t l_v318;
	bool_t l_v324; bool_t l_v327; char l_v329; long l_v291; long l_v292;
	long l_v294; long l_v295; long l_v296; long l_v301; long l_v316;
	long l_v321; long l_v322; long l_v323; long l_v331;
	struct pypy_array5 *l_v289; struct pypy_array5 *l_v304;
	struct pypy_array5 *l_v320; struct pypy_object_vtable0 *l_v326;
	struct pypy_rpy_string0 *l_v290; struct pypy_rpy_string0 *l_v333;
	void* l_v309;

    block0:
	l_v292 = (&pypy_g_list)->l_length;
	OP_INT_NE(l_v292, 0L, l_v293);
	if (l_v293) {
		goto block3;
	}
	l_v333 = (&pypy_g_rpy_string_1);
	goto block1;

    block1:
	l_v294 = pypy_g_os_write_lltypeimpl(1L, l_v333);
	goto block2;

    block2:
	RPY_DEBUG_RETURN();
	return /* nothing */;

    block3:
	l_v295 = (&pypy_g_list)->l_length;
	OP_INT_ADD(-1L, l_v295, l_v296);
	OP_INT_GE(l_v296, 0L, l_v297);
	RPyAssert(l_v297, "negative list setitem index out of bound");
	OP_INT_LT(l_v296, l_v295, l_v299);
	RPyAssert(l_v299, "list setitem index out of bound");
	l_v301 = (&pypy_g_list)->l_length;
	OP_INT_LT(l_v296, l_v301, l_v302);
	RPyAssert(l_v302, "setitem out of bounds");
	l_v304 = (&pypy_g_list)->l_items;
	l_v304->items[l_v296] = 10;
	/* kept alive: (&pypy_g_list) */ ;
	l_v291 = (&pypy_g_list)->l_length;
	l_v289 = (&pypy_g_list)->l_items;
	OP_INT_GE(l_v291, 0L, l_v307);
	RPyAssert(l_v307, "negative string length");
	l_v309 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_v291, (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, items) + (sizeof(char) * 1)), (sizeof(char) * 1), (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, length)));
	l_v290 = (struct pypy_rpy_string0 *)l_v309;
	l_v310 = (l_v290 != NULL);
	if (!l_v310) {
		goto block2;
	}
	goto block4;

    block4:
	OP_INT_IS_TRUE(MALLOC_ZERO_FILLED, l_v311);
	if (l_v311) {
		goto block6;
	}
	goto block5;

    block5:
	l_v290->rs_hash = 0L;
	goto block6;

    block6:
	l_res_chars_0 = &l_v290->rs_chars;
	l_i_6 = 0L;
	goto block7;

    block7:
	OP_INT_LT(l_i_6, l_v291, l_v313);
	if (l_v313) {
		goto block11;
	}
	goto block8;

    block8:
	/* kept alive: l_v289 */ ;
	RPyAssert(1, "del l[start:] with unexpectedly negative start");
	l_v316 = (&pypy_g_list)->l_length;
	/* kept alive: (&pypy_g_list) */ ;
	OP_INT_LE(0L, l_v316, l_v318);
	RPyAssert(l_v318, "del l[start:] with start > len(l)");
	l_v320 = (&pypy_g_list)->l_items;
	l_v321 = l_v320->length;
	OP_INT_RSHIFT(l_v321, 1L, l_v322);
	OP_INT_SUB(l_v322, 5L, l_v323);
	OP_INT_GE(0L, l_v323, l_v324);
	if (l_v324) {
		goto block10;
	}
	goto block9;

    block9:
	pypy_g__ll_list_resize_really__listPtr_Signed_1((&pypy_g_list), 0L);
	l_v326 = (&pypy_g_ExcData)->ed_exc_type;
	l_v327 = (l_v326 == NULL);
	if (!l_v327) {
		goto block2;
	}
	l_v333 = l_v290;
	goto block1;

    block10:
	(&pypy_g_list)->l_length = 0L;
	l_v333 = l_v290;
	goto block1;

    block11:
	l_v329 = l_v289->items[l_i_6];
	l_res_chars_0->items[l_i_6] = l_v329;
	OP_INT_ADD(l_i_6, 1L, l_v331);
	l_i_6 = l_v331;
	goto block7;
}
/*/*/
void pypy_g_ll_setitem_nonneg__dum_nocheckConst_listPtr_Sign(struct pypy_list0 *l_l_3, long l_index_2, struct pypy_rpy_string0 *l_newitem_0) {
	bool_t l_v334; bool_t l_v338; long l_v337; struct pypy_list0 *l_v336;
	struct pypy_list0 *l_v340;

    block0:
	OP_INT_GE(l_index_2, 0L, l_v334);
	RPyAssert(l_v334, "unexpectedly negative list setitem index");
	l_v336 = l_l_3;
	l_v337 = pypy_g_ll_length__listPtr(l_v336);
	OP_INT_LT(l_index_2, l_v337, l_v338);
	RPyAssert(l_v338, "list setitem index out of bound");
	l_v340 = l_l_3;
	pypy_g_ll_setitem_fast__listPtr_Signed_rpy_stringPtr(l_v340, l_index_2, l_newitem_0);
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return /* nothing */;
}
/*/*/
struct pypy_rpy_string0 *pypy_g_ll_getitem_fast__listPtr_Signed(struct pypy_list0 *l_l_4, long l_index_3) {
	bool_t l_v345; long l_v344; struct pypy_array0 *l_v347;
	struct pypy_rpy_string0 *l_v343;

    block0:
	l_v344 = l_l_4->l_length;
	OP_INT_LT(l_index_3, l_v344, l_v345);
	RPyAssert(l_v345, "getitem out of bounds");
	l_v347 = l_l_4->l_items;
	/* kept alive: l_l_4 */ ;
	l_v343 = l_v347->items[l_index_3];
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v343;
}
/*/*/
struct pypy_rpy_string0 *pypy_g_mallocstr__Signed(long l_length_2) {
	bool_t l_v350; bool_t l_v353; bool_t l_v354;
	struct pypy_rpy_string0 *l_v349; struct pypy_rpy_string0 *l_v356;
	void* l_v352;

    block0:
	OP_INT_GE(l_length_2, 0L, l_v350);
	RPyAssert(l_v350, "negative string length");
	l_v352 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_length_2, (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, items) + (sizeof(char) * 1)), (sizeof(char) * 1), (offsetof(struct pypy_rpy_string0, rs_chars) + offsetof(struct pypy_array1, length)));
	l_v349 = (struct pypy_rpy_string0 *)l_v352;
	l_v353 = (l_v349 != NULL);
	if (!l_v353) {
		l_v356 = ((struct pypy_rpy_string0 *) NULL);
		goto block3;
	}
	goto block1;

    block1:
	OP_INT_IS_TRUE(MALLOC_ZERO_FILLED, l_v354);
	if (l_v354) {
		l_v356 = l_v349;
		goto block3;
	}
	goto block2;

    block2:
	l_v349->rs_hash = 0L;
	l_v356 = l_v349;
	goto block3;

    block3:
	RPY_DEBUG_RETURN();
	return l_v356;
}
/*/*/
struct pypy_list0 *pypy_g_ll_newlist__GcStruct_listLlT_Signed(long l_length_3) {
	bool_t l_v359; bool_t l_v362; bool_t l_v367;
	struct pypy_array0 *l_v358; struct pypy_list0 *l_v357;
	struct pypy_list0 *l_v369; void* l_v361; void* l_v366;

    block0:
	OP_INT_GE(l_length_3, 0L, l_v359);
	RPyAssert(l_v359, "negative list length");
	l_v361 = pypy_g_ll_malloc_fixedsize__Signed_funcPtr((sizeof(struct pypy_list0) * 1), ((void (*)(void*)) NULL));
	l_v357 = (struct pypy_list0 *)l_v361;
	l_v362 = (l_v357 != NULL);
	if (!l_v362) {
		l_v369 = ((struct pypy_list0 *) NULL);
		goto block3;
	}
	goto block1;

    block1:
	l_v357->l_length = l_length_3;


	l_v366 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_length_3, (offsetof(struct pypy_array0, items) + (sizeof(struct pypy_rpy_string0 *) * 0)), (sizeof(struct pypy_rpy_string0 *) * 1), offsetof(struct pypy_array0, length));
	l_v358 = (struct pypy_array0 *)l_v366;
	l_v367 = (l_v358 != NULL);
	if (!l_v367) {
		l_v369 = ((struct pypy_list0 *) NULL);
		goto block3;
	}
	goto block2;

    block2:
	l_v357->l_items = l_v358;
	l_v369 = l_v357;
	goto block3;

    block3:
	RPY_DEBUG_RETURN();
	return l_v369;
}
/*/*/
long pypy_g_ll_length__listPtr(struct pypy_list0 *l_l_5) {
	long l_v370;

    block0:
	l_v370 = l_l_5->l_length;
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v370;
}
/*/*/
void* pypy_g_ll_malloc_fixedsize_atomic__Signed_funcPtr(long l_size_0, void (*l_finalizer_2)(void*)) {
	struct pypy_object_vtable0 *l_etype_2;
	struct pypy_object0 *l_evalue_2; void* l_result_0; bool_t l_v371;
	bool_t l_v373; void* l_v375;

    block0:
	OP_BOEHM_ZERO_MALLOC(l_size_0, l_result_0, void*, 1, 0);
	OP_ADR_NE(l_result_0, NULL, l_v371);
	if (l_v371) {
		goto block3;
	}
	l_etype_2 = (&pypy_g_exceptions_MemoryError_vtable.me_super.se_super.e_super);
	l_evalue_2 = (&pypy_g_exceptions_MemoryError_1.me_super.se_super.e_super);
	goto block1;

    block1:
	pypy_g_RPyRaiseException(l_etype_2, l_evalue_2);
	l_v375 = NULL;
	goto block2;

    block2:
	RPY_DEBUG_RETURN();
	return l_v375;

    block3:
	l_v373 = (l_finalizer_2 != NULL);
	if (l_v373) {
		goto block4;
	}
	l_v375 = l_result_0;
	goto block2;

    block4:
	GC_REGISTER_FINALIZER(l_result_0, (GC_finalization_proc)l_finalizer_2, NULL, NULL, NULL);
	l_v375 = l_result_0;
	goto block2;
}
/*/*/
void* pypy_g_ll_malloc_fixedsize__Signed_funcPtr(long l_size_1, void (*l_finalizer_1)(void*)) {
	struct pypy_object_vtable0 *l_etype_3;
	struct pypy_object0 *l_evalue_3; bool_t l_v377; bool_t l_v379;
	void* l_v376; void* l_v381;

    block0:
	OP_BOEHM_ZERO_MALLOC(l_size_1, l_v376, void*, 0, 0);
	OP_ADR_NE(l_v376, NULL, l_v377);
	if (l_v377) {
		goto block3;
	}
	l_etype_3 = (&pypy_g_exceptions_MemoryError_vtable.me_super.se_super.e_super);
	l_evalue_3 = (&pypy_g_exceptions_MemoryError_1.me_super.se_super.e_super);
	goto block1;

    block1:
	pypy_g_RPyRaiseException(l_etype_3, l_evalue_3);
	l_v381 = NULL;
	goto block2;

    block2:
	RPY_DEBUG_RETURN();
	return l_v381;

    block3:
	l_v379 = (l_finalizer_1 != NULL);
	if (l_v379) {
		goto block4;
	}
	l_v381 = l_v376;
	goto block2;

    block4:
	GC_REGISTER_FINALIZER(l_v376, (GC_finalization_proc)l_finalizer_1, NULL, NULL, NULL);
	l_v381 = l_v376;
	goto block2;
}
/*/*/
void* pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(long l_length_4, long l_size_2, long l_itemsize_0, long l_lengthoffset_0) {
	struct pypy_object_vtable0 *l_etype_4;
	struct pypy_object0 *l_evalue_4; bool_t l_v386; bool_t l_v388;
	bool_t l_v389; long l_v382; long l_v383; struct pypy_object0 *l_v393;
	struct pypy_object0 *l_v398; struct pypy_object_vtable0 *l_v385;
	struct pypy_object_vtable0 *l_v387;
	struct pypy_object_vtable0 *l_v394;
	struct pypy_object_vtable0 *l_v399; void* l_v384; void* l_v391;
	void* l_v403;

    block0:
	OP_INT_MUL_OVF(l_itemsize_0, l_length_4, l_v382);
	l_v385 = (&pypy_g_ExcData)->ed_exc_type;
	l_v386 = (l_v385 == NULL);
	if (!l_v386) {
		goto block7;
	}
	goto block1;

    block1:
	OP_INT_ADD_OVF(l_size_2, l_v382, l_v383);
	l_v387 = (&pypy_g_ExcData)->ed_exc_type;
	l_v388 = (l_v387 == NULL);
	if (!l_v388) {
		goto block6;
	}
	goto block2;

    block2:
	OP_BOEHM_ZERO_MALLOC(l_v383, l_v384, void*, 0, 0);
	OP_ADR_NE(l_v384, NULL, l_v389);
	if (l_v389) {
		goto block5;
	}
	l_evalue_4 = (&pypy_g_exceptions_MemoryError_1.me_super.se_super.e_super);
	l_etype_4 = (&pypy_g_exceptions_MemoryError_vtable.me_super.se_super.e_super);
	goto block3;

    block3:
	pypy_g_RPyRaiseException(l_etype_4, l_evalue_4);
	l_v403 = NULL;
	goto block4;

    block4:
	RPY_DEBUG_RETURN();
	return l_v403;

    block5:
	OP_ADR_ADD(l_v384, l_lengthoffset_0, l_v391);
	*(((long *) l_v391 ) + 0L) = l_length_4;
	l_v403 = l_v384;
	goto block4;

    block6:
	l_v393 = (&pypy_g_ExcData)->ed_exc_value;
	l_v394 = (&pypy_g_ExcData)->ed_exc_type;
	(&pypy_g_ExcData)->ed_exc_value = ((struct pypy_object0 *) NULL);
	(&pypy_g_ExcData)->ed_exc_type = ((struct pypy_object_vtable0 *) NULL);
	/* kept alive: l_v393 */ ;
	l_evalue_4 = (&pypy_g_exceptions_MemoryError_1.me_super.se_super.e_super);
	l_etype_4 = (&pypy_g_exceptions_MemoryError_vtable.me_super.se_super.e_super);
	goto block3;

    block7:
	l_v398 = (&pypy_g_ExcData)->ed_exc_value;
	l_v399 = (&pypy_g_ExcData)->ed_exc_type;
	(&pypy_g_ExcData)->ed_exc_value = ((struct pypy_object0 *) NULL);
	(&pypy_g_ExcData)->ed_exc_type = ((struct pypy_object_vtable0 *) NULL);
	/* kept alive: l_v398 */ ;
	l_evalue_4 = (&pypy_g_exceptions_MemoryError_1.me_super.se_super.e_super);
	l_etype_4 = (&pypy_g_exceptions_MemoryError_vtable.me_super.se_super.e_super);
	goto block3;
}
/*/*/
void pypy_g__ll_list_resize_really__listPtr_Signed(struct pypy_list1 *l_l_10, long l_newsize_2) {
	long l_new_allocated_0; long l_p_0; long l_some_0; bool_t l_v407;
	bool_t l_v411; bool_t l_v413; bool_t l_v414; bool_t l_v416;
	long l_v404; long l_v408; long l_v409; long l_v410; long l_v415;
	long l_v419; long l_v421; long l_v422; struct pypy_array3 *l_v405;
	struct pypy_array3 *l_v406; void* l_v412;

    block0:
	OP_INT_LT(l_newsize_2, 9L, l_v407);
	if (l_v407) {
		l_some_0 = 3L;
		goto block1;
	}
	l_some_0 = 6L;
	goto block1;

    block1:
	OP_INT_RSHIFT(l_newsize_2, 3L, l_v408);
	OP_INT_ADD(l_v408, l_some_0, l_v409);
	OP_INT_ADD(l_v409, l_newsize_2, l_v410);
	OP_INT_EQ(l_newsize_2, 0L, l_v411);
	if (l_v411) {
		l_new_allocated_0 = 0L;
		goto block2;
	}
	l_new_allocated_0 = l_v410;
	goto block2;

    block2:
	l_v405 = l_l_10->l_items;
	l_v412 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_new_allocated_0, (offsetof(struct pypy_array3, items) + (sizeof(long) * 0)), (sizeof(long) * 1), offsetof(struct pypy_array3, length));
	l_v406 = (struct pypy_array3 *)l_v412;
	l_v413 = (l_v406 != NULL);
	if (!l_v413) {
		goto block7;
	}
	goto block3;

    block3:
	l_v404 = l_l_10->l_length;
	OP_INT_LT(l_v404, l_new_allocated_0, l_v414);
	if (l_v414) {
		goto block9;
	}
	goto block4;

    block4:
	OP_INT_SUB(l_new_allocated_0, 1L, l_v415);
	l_p_0 = l_v415;
	goto block5;

    block5:
	OP_INT_GE(l_p_0, 0L, l_v416);
	if (l_v416) {
		goto block8;
	}
	goto block6;

    block6:
	l_l_10->l_length = l_newsize_2;
	l_l_10->l_items = l_v406;
	goto block7;

    block7:
	RPY_DEBUG_RETURN();
	return /* nothing */;

    block8:
	l_v419 = l_v405->items[l_p_0];
	l_v406->items[l_p_0] = l_v419;
	OP_INT_SUB(l_p_0, 1L, l_v421);
	l_p_0 = l_v421;
	goto block5;

    block9:
	OP_INT_SUB(l_v404, 1L, l_v422);
	l_p_0 = l_v422;
	goto block5;
}
/*/*/
void pypy_g_State_add(struct pypy_rpn_State0 *l_self_1) {
	bool_t l_v435; bool_t l_v438; bool_t l_v446; bool_t l_v449;
	bool_t l_v451; bool_t l_v455; bool_t l_v463; bool_t l_v466;
	bool_t l_v469; bool_t l_v474; bool_t l_v476; long l_v425;
	long l_v426; long l_v428; long l_v429; long l_v430; long l_v432;
	long l_v433; long l_v434; long l_v437; long l_v443; long l_v444;
	long l_v445; long l_v450; long l_v454; long l_v460; long l_v461;
	long l_v462; long l_v468; long l_v475; struct pypy_array3 *l_v440;
	struct pypy_array3 *l_v442; struct pypy_array3 *l_v457;
	struct pypy_array3 *l_v459; struct pypy_array3 *l_v467;
	struct pypy_array3 *l_v478; struct pypy_list1 *l_v424;
	struct pypy_list1 *l_v427; struct pypy_list1 *l_v431;
	struct pypy_object_vtable0 *l_v448;
	struct pypy_object_vtable0 *l_v465;
	struct pypy_object_vtable0 *l_v473;

    block0:
	l_v431 = l_self_1->s_inst_stack;
	l_v434 = l_v431->l_length;
	OP_INT_GT(l_v434, 0L, l_v435);
	RPyAssert(l_v435, "pop from empty list");
	OP_INT_SUB(l_v434, 1L, l_v429);
	l_v437 = l_v431->l_length;
	OP_INT_LT(l_v429, l_v437, l_v438);
	RPyAssert(l_v438, "getitem out of bounds");
	l_v440 = l_v431->l_items;
	l_v433 = l_v440->items[l_v429];
	/* kept alive: l_v431 */ ;
	l_v442 = l_v431->l_items;
	l_v443 = l_v442->length;
	OP_INT_RSHIFT(l_v443, 1L, l_v444);
	OP_INT_SUB(l_v444, 5L, l_v445);
	OP_INT_GE(l_v429, l_v445, l_v446);
	if (l_v446) {
		goto block10;
	}
	goto block1;

    block1:
	pypy_g__ll_list_resize_really__listPtr_Signed(l_v431, l_v429);
	l_v448 = (&pypy_g_ExcData)->ed_exc_type;
	l_v449 = (l_v448 == NULL);
	if (!l_v449) {
		goto block7;
	}
	goto block2;

    block2:
	l_v427 = l_self_1->s_inst_stack;
	l_v450 = l_v427->l_length;
	OP_INT_GT(l_v450, 0L, l_v451);
	/* kept alive: l_v431 */ ;
	RPyAssert(l_v451, "pop from empty list");
	OP_INT_SUB(l_v450, 1L, l_v432);
	l_v454 = l_v427->l_length;
	OP_INT_LT(l_v432, l_v454, l_v455);
	RPyAssert(l_v455, "getitem out of bounds");
	l_v457 = l_v427->l_items;
	l_v430 = l_v457->items[l_v432];
	/* kept alive: l_v427 */ ;
	l_v459 = l_v427->l_items;
	l_v460 = l_v459->length;
	OP_INT_RSHIFT(l_v460, 1L, l_v461);
	OP_INT_SUB(l_v461, 5L, l_v462);
	OP_INT_GE(l_v432, l_v462, l_v463);
	if (l_v463) {
		goto block9;
	}
	goto block3;

    block3:
	pypy_g__ll_list_resize_really__listPtr_Signed(l_v427, l_v432);
	l_v465 = (&pypy_g_ExcData)->ed_exc_type;
	l_v466 = (l_v465 == NULL);
	if (!l_v466) {
		goto block7;
	}
	goto block4;

    block4:
	l_v424 = l_self_1->s_inst_stack;
	OP_INT_ADD(l_v430, l_v433, l_v426);
	l_v428 = l_v424->l_length;
	OP_INT_ADD(l_v428, 1L, l_v425);
	l_v467 = l_v424->l_items;
	l_v468 = l_v467->length;
	OP_INT_GE(l_v468, l_v425, l_v469);
	/* kept alive: l_v427 */ ;
	/* kept alive: l_v424 */ ;
	if (l_v469) {
		goto block8;
	}
	goto block5;

    block5:
	pypy_g__ll_list_resize_really__listPtr_Signed(l_v424, l_v425);
	l_v473 = (&pypy_g_ExcData)->ed_exc_type;
	l_v474 = (l_v473 == NULL);
	if (!l_v474) {
		goto block7;
	}
	goto block6;

    block6:
	l_v475 = l_v424->l_length;
	OP_INT_LT(l_v428, l_v475, l_v476);
	RPyAssert(l_v476, "setitem out of bounds");
	l_v478 = l_v424->l_items;
	l_v478->items[l_v428] = l_v426;
	/* kept alive: l_v424 */ ;
	goto block7;

    block7:
	RPY_DEBUG_RETURN();
	return /* nothing */;

    block8:
	l_v424->l_length = l_v425;
	goto block6;

    block9:
	l_v427->l_length = l_v432;
	goto block4;

    block10:
	l_v431->l_length = l_v429;
	goto block2;
}
/*/*/
void pypy_g__ll_list_resize_really__listPtr_Signed_1(struct pypy_list2 *l_l_11, long l_newsize_3) {
	long l_new_allocated_1; long l_p_1; long l_some_1; bool_t l_v488;
	bool_t l_v492; bool_t l_v494; bool_t l_v495; bool_t l_v497;
	char l_v500; long l_v486; long l_v489; long l_v490; long l_v491;
	long l_v496; long l_v502; long l_v503; struct pypy_array5 *l_v485;
	struct pypy_array5 *l_v487; void* l_v493;

    block0:
	OP_INT_LT(l_newsize_3, 9L, l_v488);
	if (l_v488) {
		l_some_1 = 3L;
		goto block1;
	}
	l_some_1 = 6L;
	goto block1;

    block1:
	OP_INT_RSHIFT(l_newsize_3, 3L, l_v489);
	OP_INT_ADD(l_v489, l_some_1, l_v490);
	OP_INT_ADD(l_v490, l_newsize_3, l_v491);
	OP_INT_EQ(l_newsize_3, 0L, l_v492);
	if (l_v492) {
		l_new_allocated_1 = 0L;
		goto block2;
	}
	l_new_allocated_1 = l_v491;
	goto block2;

    block2:
	l_v487 = l_l_11->l_items;
	l_v493 = pypy_g_ll_malloc_varsize__Signed_Signed_Signed_Signed(l_new_allocated_1, (offsetof(struct pypy_array5, items) + (sizeof(char) * 0)), (sizeof(char) * 1), offsetof(struct pypy_array5, length));
	l_v485 = (struct pypy_array5 *)l_v493;
	l_v494 = (l_v485 != NULL);
	if (!l_v494) {
		goto block7;
	}
	goto block3;

    block3:
	l_v486 = l_l_11->l_length;
	OP_INT_LT(l_v486, l_new_allocated_1, l_v495);
	if (l_v495) {
		goto block9;
	}
	goto block4;

    block4:
	OP_INT_SUB(l_new_allocated_1, 1L, l_v496);
	l_p_1 = l_v496;
	goto block5;

    block5:
	OP_INT_GE(l_p_1, 0L, l_v497);
	if (l_v497) {
		goto block8;
	}
	goto block6;

    block6:
	l_l_11->l_length = l_newsize_3;
	l_l_11->l_items = l_v485;
	goto block7;

    block7:
	RPY_DEBUG_RETURN();
	return /* nothing */;

    block8:
	l_v500 = l_v487->items[l_p_1];
	l_v485->items[l_p_1] = l_v500;
	OP_INT_SUB(l_p_1, 1L, l_v502);
	l_p_1 = l_v502;
	goto block5;

    block9:
	OP_INT_SUB(l_v486, 1L, l_v503);
	l_p_1 = l_v503;
	goto block5;
}
/*/*/
long pypy_g_os_write_lltypeimpl(long l_fd_1, struct pypy_rpy_string0 *l_data_1) {
	struct pypy_array6 *l_outbuf_0; bool_t l_v514; bool_t l_v516;
	bool_t l_v519; bool_t l_v522; bool_t l_v525; bool_t l_v536;
	bool_t l_v538; bool_t l_v541; char l_v527; long l_v505; long l_v509;
	long l_v510; long l_v511; long l_v518; long l_v524; long l_v555;
	struct pypy_array1 *l_v512; struct pypy_array1 *l_v517;
	struct pypy_array1 *l_v521;
	struct pypy_exceptions_Exception0 *l_v546;
	struct pypy_exceptions_Exception0 *l_v554;
	struct pypy_exceptions_Exception0 *l_v557;
	struct pypy_exceptions_OSError0 *l_v508; struct pypy_object0 *l_v532;
	struct pypy_object0 *l_v542; struct pypy_object0 *l_v548;
	struct pypy_object_vtable0 *l_v513;
	struct pypy_object_vtable0 *l_v535;
	struct pypy_object_vtable0 *l_v545;
	struct pypy_object_vtable0 *l_v549;
	struct pypy_object_vtable0 *l_v556; unsigned long l_v506;
	unsigned long l_v507; void* l_v540;

    block0:
	l_v512 = &l_data_1->rs_chars;
	l_v509 = l_v512->length;
	IF_VARSIZE_OVERFLOW(l_v509, char, l_outbuf_0)
	else {
	OP_RAW_MALLOC(sizeof(struct pypy_array6)-sizeof(char)+l_v509*sizeof(char), l_outbuf_0, struct pypy_array6 *);
	}
	l_v513 = (&pypy_g_ExcData)->ed_exc_type;
	l_v514 = (l_v513 == NULL);
	if (!l_v514) {
		l_v555 = -1L;
		goto block7;
	}
	goto block1;

    block1:
	/* kept alive: l_data_1 */ ;
	l_v505 = 0L;
	goto block2;

    block2:
	OP_INT_GE(l_v505, l_v509, l_v516);
	if (l_v516) {
		goto block8;
	}
	goto block3;

    block3:
	OP_INT_ADD(l_v505, 1L, l_v510);
	l_v517 = &l_data_1->rs_chars;
	l_v518 = l_v517->length;
	OP_INT_GE(l_v505, l_v518, l_v519);
	/* kept alive: l_data_1 */ ;
	if (l_v519) {
		goto block5;
	}
	goto block4;

    block4:
	l_v521 = &l_data_1->rs_chars;
	OP_INT_GE(l_v505, 0L, l_v522);
	RPyAssert(l_v522, "negative str getitem index");
	l_v524 = l_v521->length;
	OP_INT_LT(l_v505, l_v524, l_v525);
	RPyAssert(l_v525, "str getitem index out of bound");
	l_v527 = l_v521->items[l_v505];
	/* kept alive: l_data_1 */ ;
	l_outbuf_0->items[l_v505] = l_v527;
	l_v505 = l_v510;
	goto block2;

    block5:
	/* kept alive: l_data_1 */ ;
	l_v557 = (&pypy_g_exceptions_IndexError.ie_super.le_super.se_super);
	l_v556 = (&pypy_g_exceptions_IndexError_vtable.ie_super.le_super.se_super.e_super);
	goto block6;

    block6:
	OP_RAW_FREE(l_outbuf_0, /* nothing */)
	l_v532 = (struct pypy_object0 *)l_v557;
	pypy_g_RPyRaiseException(l_v556, l_v532);
	l_v555 = -1L;
	goto block7;

    block7:
	RPY_DEBUG_RETURN();
	return l_v555;

    block8:
	OP_CAST_INT_TO_UINT(l_v509, l_v506);
	/* kept alive: l_data_1 */ ;
	l_v507 = write(l_fd_1, l_outbuf_0, l_v506);
	l_v535 = (&pypy_g_ExcData)->ed_exc_type;
	l_v536 = (l_v535 == NULL);
	if (!l_v536) {
		goto block13;
	}
	goto block9;

    block9:
	/* kept alive: l_data_1 */ ;
	OP_CAST_UINT_TO_INT(l_v507, l_v511);
	OP_INT_LT(l_v511, 0L, l_v538);
	if (l_v538) {
		goto block11;
	}
	goto block10;

    block10:
	OP_RAW_FREE(l_outbuf_0, /* nothing */)
	l_v555 = l_v511;
	goto block7;

    block11:
	l_v540 = pypy_g_ll_malloc_fixedsize_atomic__Signed_funcPtr((sizeof(struct pypy_exceptions_OSError0) * 1), ((void (*)(void*)) NULL));
	l_v508 = (struct pypy_exceptions_OSError0 *)l_v540;
	l_v541 = (l_v508 != NULL);
	if (!l_v541) {
		l_v555 = -1L;
		goto block7;
	}
	goto block12;

    block12:
	l_v542 = (struct pypy_object0 *)l_v508;
	l_v542->o_typeptr = (&pypy_g_exceptions_OSError_vtable.ose_super.ee_super.se_super.e_super);
	l_v508->ose_inst_errno = errno;
	l_v545 = l_v542->o_typeptr;
	l_v546 = (struct pypy_exceptions_Exception0 *)l_v508;
	/* kept alive: l_v508 */ ;
	l_v557 = l_v546;
	l_v556 = l_v545;
	goto block6;

    block13:
	l_v548 = (&pypy_g_ExcData)->ed_exc_value;
	l_v549 = (&pypy_g_ExcData)->ed_exc_type;
	(&pypy_g_ExcData)->ed_exc_value = ((struct pypy_object0 *) NULL);
	(&pypy_g_ExcData)->ed_exc_type = ((struct pypy_object_vtable0 *) NULL);
	/* kept alive: l_v548 */ ;
	/* kept alive: l_data_1 */ ;
	l_v554 = (struct pypy_exceptions_Exception0 *)l_v548;
	l_v557 = l_v554;
	l_v556 = l_v549;
	goto block6;
}
/*/*/
void pypy_g_ll_setitem_fast__listPtr_Signed_rpy_stringPtr(struct pypy_list0 *l_l_8, long l_index_4, struct pypy_rpy_string0 *l_item_0) {
	bool_t l_v559; long l_v558; struct pypy_array0 *l_v562;
	struct pypy_list0 *l_v561;

    block0:
	l_v558 = l_l_8->l_length;
	OP_INT_LT(l_index_4, l_v558, l_v559);
	RPyAssert(l_v559, "setitem out of bounds");
	l_v561 = l_l_8;
	l_v562 = pypy_g_ll_items__listPtr(l_v561);
	l_v562->items[l_index_4] = l_item_0;
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return /* nothing */;
}
/*/*/

/*/*/
struct pypy_array0 *pypy_g_ll_items__listPtr(struct pypy_list0 *l_l_9) {
	struct pypy_array0 *l_v565;

    block0:
	l_v565 = l_l_9->l_items;
	goto block1;

    block1:
	RPY_DEBUG_RETURN();
	return l_v565;
}
/*/*/
/***********************************************************/
