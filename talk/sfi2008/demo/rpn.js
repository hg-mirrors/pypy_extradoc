// starts hand written code
MALLOC_ZERO_FILLED = 0

try {
    log;
    print = log;
} catch(e) {
}

Function.prototype.method = function (name, func) {
    this.prototype[name] = func;
    return this;
};

function inherits(child, parent) {
    child.parent = parent;
    for (i in parent.prototype) {
        if (!child.prototype[i]) {
            child.prototype[i] = parent.prototype[i];
        }
    }
}

function isinstanceof(self, what) {
    if (!self) {
        return (false);
    }
    t = self.constructor;
    while ( t ) {
        if (t == what) {
            return (true);
        }
        t = t.parent;
    }
    return (false);
}

/*function delitem(fn, l, i) {
    for(j = i; j < l.length-1; ++j) {
        l[j] = l[j+1];
    }
    l.length--;
}*/

function strcmp(s1, s2) {
    if ( s1 < s2 ) {
        return ( -1 );
    } else if ( s1 == s2 ) {
        return ( 0 );
    }
    return (1);
}

function startswith(s1, s2) {
    if (s1.length < s2.length) {
        return(false);
    }
    for (i = 0; i < s2.length; ++i){
        if (s1.charAt(i) != s2.charAt(i)) {
            return(false);
        }
    }
    return(true);
}

function endswith(s1, s2) {
    if (s2.length > s1.length) {
        return(false);
    }
    for (i = s1.length-s2.length; i < s1.length; ++i) {
        if (s1.charAt(i) != s2.charAt(i - s1.length + s2.length)) {
            return(false);
        }
    }
    return(true);
}

function splitchr(s, ch) {
    var i, lst, next;
    lst = [];
    next = "";
    for (i = 0; i<s.length; ++i) {
        if (s.charAt(i) == ch) {
            lst.length += 1;
            lst[lst.length-1] = next;
            next = "";
        } else {
            next += s.charAt(i);
        }
    }
    lst.length += 1;
    lst[lst.length-1] = next;
    return (lst);
}

function DictIter() {
}

DictIter.prototype.ll_go_next = function () {
    var ret = this.l.length != 0;
    this.current_key = this.l.pop();
    return ret;
}

DictIter.prototype.ll_current_key = function () {
    return this.current_key;
}

function dict_items_iterator(d) {
    var d2 = new DictIter();
    var l = [];
    for (var i in d) {
        l.length += 1;
        l[l.length-1] = i;
    }
    d2.l = l;
    d2.current_key = undefined;
    return d2;
}

function get_dict_len(d) {
    var count;
    count = 0;
    for (var i in d) {
        count += 1;
    }
    return (count);
}

function StringBuilder() {
    this.l = [];
}

StringBuilder.prototype.ll_append_char = function(s) {
    this.l.length += 1;
    this.l[this.l.length - 1] = s;
}

StringBuilder.prototype.ll_append = function(s) {
    this.l.push(s);
}

StringBuilder.prototype.ll_allocate = function(t) {
}

StringBuilder.prototype.ll_build = function() {
    var s;
    s = "";
    for (i in this.l) {
        s += this.l[i];
    }
    return (s);
}

function time() {
    var d;
    d = new Date();
    return d/1000;
}

var main_clock_stuff;

function clock() {
    if (main_clock_stuff) {
        return (new Date() - main_clock_stuff)/1000;
    } else {
        main_clock_stuff = new Date();
        return 0;
    }
}

function substring(s, l, c) {
    return (s.substring(l, l+c));
}

function clear_dict(d) {
    for (var elem in d) {
        delete(d[elem]);
    }
}

function findIndexOf(s1, s2, start, end) {
    if (start > end || start > s1.length) {
        return -1;
    }
    s1 = s1.substr(start, end-start);
    res = s1.indexOf(s2);
    if (res == -1) {
        return -1;
    }
    return res + start;
}

function findIndexOfTrue(s1, s2) {
    return findIndexOf(s1, s2, 0, s1.length) != -1;
}

function countCharOf(s, c, start, end) {
    s = s.substring(start, end);
    var i = 0;
    for (c1 in s) {
        if (s[c1] == c) {
            i++;
        }
    }
    return(i);
}

function countOf(s, s1, start, end) {
    var ret = findIndexOf(s, s1, start, end);
    var i = 0;
    var lgt = 1;
    if (s1.length > 0) {
        lgt = s1.length;
    }
    while (ret != -1) {
        i++;
        ret = findIndexOf(s, s1, ret + lgt, end);
    }
    return (i);
}

function convertToString(stuff) {
    if (stuff === undefined) {
       return ("undefined");
    }
    return (stuff.toString());
}    
// ends hand written code
function entry_point (argv_0) {
    var v0,v1,v2,v3,v4;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v1 = ll_getitem_nonneg__dum_nocheckConst_List_String__Signed ( argv_0,1 );
            v2 = ll_getitem_nonneg__dum_nocheckConst_List_String__Signed ( argv_0,2 );
            v3 = ll_int__String_Signed ( v2,10 );
            v4 = interpret ( v1,v3 );
            v0 = 0;
            block = 1;
            break;
            case 1:
            return ( v0 );
        }
    }
}

function interpret (code_0,arg_0) {
    var v117,v118,v121,v123,state_0,v124,v125,last_exc_value_0,c_8,state_1,v126,v127,v128,state_2,v129,v130,v131,v132,state_3,v133,v134,c_9,state_4,v136,v137,c_10,state_5,v138,v139,v140,c_11,state_6,v141,v142,v143,v144,v146,v147,v148;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v118 = new rpn_State();
            v118.meta = __consts_0.rpn_State_meta;
            State___init__ ( v118 );
            v118.opush(arg_0);
            v123 = ll_striter__String ( code_0 );
            state_0 = v118;
            v124 = v123;
            block = 1;
            break;
            case 1:
            try {
                v125 = ll_strnext__Record_index__Signed__string__ ( v124 );
                c_8 = v125;
                state_1 = state_0;
                v126 = v124;
                block = 2;
                break;
            }
            catch (exc){
                if (isinstanceof(exc, exceptions_StopIteration))
                {
                    v146 = state_0;
                    block = 8;
                    break;
                }
                throw(exc);
            }
            case 2:
            v127 = ('0'<=c_8);
            state_2 = state_1;
            v129 = v126;
            v130 = c_8;
            if (v127 == false)
            {
                block = 3;
                break;
            }
            c_9 = c_8;
            state_4 = state_1;
            v136 = v126;
            block = 5;
            break;
            case 3:
            v131 = (v130=='+');
            state_0 = state_2;
            v124 = v129;
            if (v131 == false)
            {
                block = 1;
                break;
            }
            state_3 = state_2;
            v133 = v129;
            block = 4;
            break;
            case 4:
            state_3.oadd();
            state_0 = state_3;
            v124 = v133;
            block = 1;
            break;
            case 5:
            v137 = (c_9<='9');
            c_10 = c_9;
            state_5 = state_4;
            v138 = v136;
            v139 = v137;
            block = 6;
            break;
            case 6:
            state_2 = state_5;
            v129 = v138;
            v130 = c_10;
            if (v139 == false)
            {
                block = 3;
                break;
            }
            c_11 = c_10;
            state_6 = state_5;
            v141 = v138;
            block = 7;
            break;
            case 7:
            v143 = c_11.charCodeAt(0);
            v144 = (v143-48);
            state_6.opush(v144);
            state_0 = state_6;
            v124 = v141;
            block = 1;
            break;
            case 8:
            v148 = v146.ogetresult();
            v117 = v148;
            block = 9;
            break;
            case 9:
            return ( v117 );
        }
    }
}

function ll_strnext__Record_index__Signed__string__ (iter_0) {
    var v157,v158,v159,v160,v161,v162,v163,iter_1,index_3,string_1,v164,v166,v167,v168,v169,v170,etype_1,evalue_1;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v158 = iter_0.string;
            v159 = iter_0.index;
            v161 = v158.length;
            v162 = (v159>=v161);
            iter_1 = iter_0;
            index_3 = v159;
            string_1 = v158;
            if (v162 == false)
            {
                block = 1;
                break;
            }
            block = 3;
            break;
            case 1:
            v164 = (index_3+1);
            iter_1.index = v164;
            v167 = string_1.charAt(index_3);
            v157 = v167;
            block = 2;
            break;
            case 3:
            v168 = __consts_0.exceptions_StopIteration;
            v169 = v168.meta;
            etype_1 = v169;
            evalue_1 = v168;
            block = 4;
            break;
            case 4:
            throw(evalue_1);
            case 2:
            return ( v157 );
        }
    }
}

function rpn_State () {
    this.ostack = __consts_0.const_list;
}

rpn_State.prototype.toString = function (){
    return ( '<rpn.State object>' );
}

inherits(rpn_State,Object);
rpn_State.prototype.oadd = function (){
    var v172,v173,v174,v175,v176,v177,v178,v179,v180;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v172 = this.ostack;
            v174 = ll_pop_default__dum_nocheckConst_List_Signed_ ( v172 );
            v175 = this.ostack;
            v177 = ll_pop_default__dum_nocheckConst_List_Signed_ ( v175 );
            v178 = this.ostack;
            v180 = (v177+v174);
            ll_append__List_Signed__Signed ( v178,v180 );
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

rpn_State.prototype.ogetresult = function (){
    var v202,v203,v204;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v203 = this.ostack;
            v204 = ll_getitem__dum_nocheckConst_List_Signed__Signed ( v203,-1 );
            v202 = v204;
            block = 1;
            break;
            case 1:
            return ( v202 );
        }
    }
}

rpn_State.prototype.opush = function (value_0){
    var v220,v221;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v220 = this.ostack;
            ll_append__List_Signed__Signed ( v220,value_0 );
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

rpn_State.prototype.o__init__ = function (){
    var v150;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v150 = new Array();
            v150.length = 0;
            this.ostack = v150;
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

function ll_getitem_nonneg__dum_nocheckConst_List_String__Signed (l_0,index_0) {
    var v5,v6,l_1,index_1,v8,v9,v10,index_2,v12,v13,v14;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v6 = (index_0>=0);
            l_1 = l_0;
            index_1 = index_0;
            block = 1;
            break;
            case 1:
            v9 = l_1.length;
            v10 = (index_1<v9);
            index_2 = index_1;
            v12 = l_1;
            block = 2;
            break;
            case 2:
            v14 = v12[index_2];
            v5 = v14;
            block = 3;
            break;
            case 3:
            return ( v5 );
        }
    }
}

function Object_meta () {
    this.class_ = __consts_0.None;
}

Object_meta.prototype.toString = function (){
    return ( '<Object_meta object>' );
}

function rpn_State_meta () {
}

rpn_State_meta.prototype.toString = function (){
    return ( '<rpn.State_meta object>' );
}

inherits(rpn_State_meta,Object_meta);
function ll_pop_default__dum_nocheckConst_List_Signed_ (l_2) {
    var v182,v183,v184,l_3,length_0,v185,v187,v188,v189,res_0,newlength_0,v191,v192;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v184 = l_2.length;
            l_3 = l_2;
            length_0 = v184;
            block = 1;
            break;
            case 1:
            v185 = (length_0>0);
            v187 = (length_0-1);
            v189 = l_3[v187];
            ll_null_item__List_Signed_ ( l_3 );
            res_0 = v189;
            newlength_0 = v187;
            v191 = l_3;
            block = 2;
            break;
            case 2:
            v191.length = newlength_0;
            v182 = res_0;
            block = 3;
            break;
            case 3:
            return ( v182 );
        }
    }
}

function exceptions_Exception () {
}

exceptions_Exception.prototype.toString = function (){
    return ( '<exceptions.Exception object>' );
}

inherits(exceptions_Exception,Object);
function ll_getitem__dum_nocheckConst_List_Signed__Signed (l_5,index_4) {
    var v205,v206,v207,v208,v209,l_6,index_5,length_1,v210,v212,index_6,v214,v215,v216,l_7,length_2,v217,v218;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v207 = l_5.length;
            v208 = (index_4<0);
            l_6 = l_5;
            index_5 = index_4;
            length_1 = v207;
            if (v208 == false)
            {
                block = 1;
                break;
            }
            l_7 = l_5;
            length_2 = v207;
            v217 = index_4;
            block = 4;
            break;
            case 1:
            v210 = (index_5>=0);
            v212 = (index_5<length_1);
            index_6 = index_5;
            v214 = l_6;
            block = 2;
            break;
            case 2:
            v216 = v214[index_6];
            v205 = v216;
            block = 3;
            break;
            case 4:
            v218 = (v217+length_2);
            l_6 = l_7;
            index_5 = v218;
            length_1 = length_2;
            block = 1;
            break;
            case 3:
            return ( v205 );
        }
    }
}

function ll_append__List_Signed__Signed (l_4,newitem_0) {
    var v195,v196,v197,v198,v200;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v196 = l_4.length;
            v198 = (v196+1);
            l_4.length = v198;
            l_4[v196]=newitem_0;
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

function ll_int__String_Signed (s_0,base_0) {
    var v15,v16,v17,v18,v19,v20,etype_0,evalue_0,s_1,base_1,v21,s_2,base_2,v22,v23,s_3,base_3,v24,v25,s_4,base_4,i_0,strlen_0,v26,v27,s_5,base_5,i_1,strlen_1,v28,v29,v30,v31,v32,s_6,base_6,i_2,strlen_2,v33,v34,v35,v36,s_7,base_7,i_3,strlen_3,v37,v38,v39,v40,s_8,base_8,i_4,sign_0,strlen_4,v41,v42,s_9,base_9,val_0,i_5,sign_1,oldpos_0,strlen_5,v43,v44,s_10,val_1,i_6,sign_2,strlen_6,v45,v46,v47,s_11,val_2,i_7,sign_3,strlen_7,v48,v49,val_3,sign_4,v50,v51,v52,v53,v54,v55,v56,v57,v58,v59,s_12,val_4,i_8,sign_5,strlen_8,v60,v61,v62,v63,s_13,val_5,sign_6,strlen_9,v64,v65,v66,v67,v68,s_14,base_10,val_6,i_9,sign_7,oldpos_1,strlen_10,v69,v70,v71,v72,v73,s_15,base_11,c_0,val_7,i_10,sign_8,oldpos_2,strlen_11,v74,v75,s_16,base_12,c_1,val_8,i_11,sign_9,oldpos_3,strlen_12,v76,v77,s_17,base_13,c_2,val_9,i_12,sign_10,oldpos_4,strlen_13,v78,s_18,base_14,c_3,val_10,i_13,sign_11,oldpos_5,strlen_14,v79,v80,s_19,base_15,val_11,i_14,sign_12,oldpos_6,strlen_15,v81,v82,s_20,base_16,val_12,i_15,digit_0,sign_13,oldpos_7,strlen_16,v83,v84,s_21,base_17,i_16,digit_1,sign_14,oldpos_8,strlen_17,v85,v86,v87,v88,s_22,base_18,c_4,val_13,i_17,sign_15,oldpos_9,strlen_18,v89,s_23,base_19,c_5,val_14,i_18,sign_16,oldpos_10,strlen_19,v90,v91,s_24,base_20,val_15,i_19,sign_17,oldpos_11,strlen_20,v92,v93,v94,s_25,base_21,c_6,val_16,i_20,sign_18,oldpos_12,strlen_21,v95,s_26,base_22,c_7,val_17,i_21,sign_19,oldpos_13,strlen_22,v96,v97,s_27,base_23,val_18,i_22,sign_20,oldpos_14,strlen_23,v98,v99,v100,s_28,base_24,i_23,sign_21,strlen_24,v101,v102,v103,v104,s_29,base_25,sign_22,strlen_25,v105,v106,s_30,base_26,strlen_26,v107,v108,s_31,base_27,strlen_27,v109,v110,s_32,base_28,i_24,strlen_28,v111,v112,v113,v114,s_33,base_29,strlen_29,v115,v116;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v16 = (2<=base_0);
            if (v16 == false)
            {
                block = 1;
                break;
            }
            s_1 = s_0;
            base_1 = base_0;
            block = 3;
            break;
            case 1:
            v18 = __consts_0.exceptions_ValueError;
            v19 = v18.meta;
            etype_0 = v19;
            evalue_0 = v18;
            block = 2;
            break;
            case 3:
            v21 = (base_1<=36);
            s_2 = s_1;
            base_2 = base_1;
            v22 = v21;
            block = 4;
            break;
            case 4:
            if (v22 == false)
            {
                block = 1;
                break;
            }
            s_3 = s_2;
            base_3 = base_2;
            block = 5;
            break;
            case 5:
            v25 = s_3.length;
            s_4 = s_3;
            base_4 = base_3;
            i_0 = 0;
            strlen_0 = v25;
            block = 6;
            break;
            case 6:
            v26 = (i_0<strlen_0);
            s_5 = s_4;
            base_5 = base_4;
            i_1 = i_0;
            strlen_1 = strlen_0;
            if (v26 == false)
            {
                block = 7;
                break;
            }
            s_32 = s_4;
            base_28 = base_4;
            i_24 = i_0;
            strlen_28 = strlen_0;
            block = 40;
            break;
            case 7:
            v28 = (i_1<strlen_1);
            if (v28 == false)
            {
                block = 8;
                break;
            }
            s_6 = s_5;
            base_6 = base_5;
            i_2 = i_1;
            strlen_2 = strlen_1;
            block = 9;
            break;
            case 8:
            v30 = __consts_0.exceptions_ValueError;
            v31 = v30.meta;
            etype_0 = v31;
            evalue_0 = v30;
            block = 2;
            break;
            case 9:
            v34 = s_6.charAt(i_2);
            v35 = (v34=='-');
            s_7 = s_6;
            base_7 = base_6;
            i_3 = i_2;
            strlen_3 = strlen_2;
            if (v35 == false)
            {
                block = 10;
                break;
            }
            s_31 = s_6;
            base_27 = base_6;
            strlen_27 = strlen_2;
            v109 = i_2;
            block = 39;
            break;
            case 10:
            v38 = s_7.charAt(i_3);
            v39 = (v38=='+');
            s_8 = s_7;
            base_8 = base_7;
            i_4 = i_3;
            sign_0 = 1;
            strlen_4 = strlen_3;
            if (v39 == false)
            {
                block = 11;
                break;
            }
            s_30 = s_7;
            base_26 = base_7;
            strlen_26 = strlen_3;
            v107 = i_3;
            block = 38;
            break;
            case 11:
            v41 = (i_4<strlen_4);
            s_9 = s_8;
            base_9 = base_8;
            val_0 = 0;
            i_5 = i_4;
            sign_1 = sign_0;
            oldpos_0 = i_4;
            strlen_5 = strlen_4;
            if (v41 == false)
            {
                block = 12;
                break;
            }
            s_28 = s_8;
            base_24 = base_8;
            i_23 = i_4;
            sign_21 = sign_0;
            strlen_24 = strlen_4;
            block = 36;
            break;
            case 12:
            v43 = (i_5<strlen_5);
            s_10 = s_9;
            val_1 = val_0;
            i_6 = i_5;
            sign_2 = sign_1;
            strlen_6 = strlen_5;
            v45 = oldpos_0;
            if (v43 == false)
            {
                block = 13;
                break;
            }
            s_14 = s_9;
            base_10 = base_9;
            val_6 = val_0;
            i_9 = i_5;
            sign_7 = sign_1;
            oldpos_1 = oldpos_0;
            strlen_10 = strlen_5;
            block = 22;
            break;
            case 13:
            v46 = (i_6==v45);
            s_11 = s_10;
            val_2 = val_1;
            i_7 = i_6;
            sign_3 = sign_2;
            strlen_7 = strlen_6;
            if (v46 == false)
            {
                block = 14;
                break;
            }
            block = 21;
            break;
            case 14:
            v48 = (i_7<strlen_7);
            val_3 = val_2;
            sign_4 = sign_3;
            v50 = i_7;
            v51 = strlen_7;
            if (v48 == false)
            {
                block = 15;
                break;
            }
            s_12 = s_11;
            val_4 = val_2;
            i_8 = i_7;
            sign_5 = sign_3;
            strlen_8 = strlen_7;
            block = 19;
            break;
            case 15:
            v52 = (v50==v51);
            if (v52 == false)
            {
                block = 16;
                break;
            }
            v57 = sign_4;
            v58 = val_3;
            block = 17;
            break;
            case 16:
            v54 = __consts_0.exceptions_ValueError;
            v55 = v54.meta;
            etype_0 = v55;
            evalue_0 = v54;
            block = 2;
            break;
            case 17:
            v59 = (v57*v58);
            v15 = v59;
            block = 18;
            break;
            case 19:
            v61 = s_12.charAt(i_8);
            v62 = (v61==' ');
            val_3 = val_4;
            sign_4 = sign_5;
            v50 = i_8;
            v51 = strlen_8;
            if (v62 == false)
            {
                block = 15;
                break;
            }
            s_13 = s_12;
            val_5 = val_4;
            sign_6 = sign_5;
            strlen_9 = strlen_8;
            v64 = i_8;
            block = 20;
            break;
            case 20:
            v65 = (v64+1);
            s_11 = s_13;
            val_2 = val_5;
            i_7 = v65;
            sign_3 = sign_6;
            strlen_7 = strlen_9;
            block = 14;
            break;
            case 21:
            v66 = __consts_0.exceptions_ValueError;
            v67 = v66.meta;
            etype_0 = v67;
            evalue_0 = v66;
            block = 2;
            break;
            case 22:
            v70 = s_14.charAt(i_9);
            v71 = v70.charCodeAt(0);
            v72 = (97<=v71);
            s_15 = s_14;
            base_11 = base_10;
            c_0 = v71;
            val_7 = val_6;
            i_10 = i_9;
            sign_8 = sign_7;
            oldpos_2 = oldpos_1;
            strlen_11 = strlen_10;
            if (v72 == false)
            {
                block = 23;
                break;
            }
            s_25 = s_14;
            base_21 = base_10;
            c_6 = v71;
            val_16 = val_6;
            i_20 = i_9;
            sign_18 = sign_7;
            oldpos_12 = oldpos_1;
            strlen_21 = strlen_10;
            block = 33;
            break;
            case 23:
            v74 = (65<=c_0);
            s_16 = s_15;
            base_12 = base_11;
            c_1 = c_0;
            val_8 = val_7;
            i_11 = i_10;
            sign_9 = sign_8;
            oldpos_3 = oldpos_2;
            strlen_12 = strlen_11;
            if (v74 == false)
            {
                block = 24;
                break;
            }
            s_22 = s_15;
            base_18 = base_11;
            c_4 = c_0;
            val_13 = val_7;
            i_17 = i_10;
            sign_15 = sign_8;
            oldpos_9 = oldpos_2;
            strlen_18 = strlen_11;
            block = 30;
            break;
            case 24:
            v76 = (48<=c_1);
            s_10 = s_16;
            val_1 = val_8;
            i_6 = i_11;
            sign_2 = sign_9;
            strlen_6 = strlen_12;
            v45 = oldpos_3;
            if (v76 == false)
            {
                block = 13;
                break;
            }
            s_17 = s_16;
            base_13 = base_12;
            c_2 = c_1;
            val_9 = val_8;
            i_12 = i_11;
            sign_10 = sign_9;
            oldpos_4 = oldpos_3;
            strlen_13 = strlen_12;
            block = 25;
            break;
            case 25:
            v78 = (c_2<=57);
            s_18 = s_17;
            base_14 = base_13;
            c_3 = c_2;
            val_10 = val_9;
            i_13 = i_12;
            sign_11 = sign_10;
            oldpos_5 = oldpos_4;
            strlen_14 = strlen_13;
            v79 = v78;
            block = 26;
            break;
            case 26:
            s_10 = s_18;
            val_1 = val_10;
            i_6 = i_13;
            sign_2 = sign_11;
            strlen_6 = strlen_14;
            v45 = oldpos_5;
            if (v79 == false)
            {
                block = 13;
                break;
            }
            s_19 = s_18;
            base_15 = base_14;
            val_11 = val_10;
            i_14 = i_13;
            sign_12 = sign_11;
            oldpos_6 = oldpos_5;
            strlen_15 = strlen_14;
            v81 = c_3;
            block = 27;
            break;
            case 27:
            v82 = (v81-48);
            s_20 = s_19;
            base_16 = base_15;
            val_12 = val_11;
            i_15 = i_14;
            digit_0 = v82;
            sign_13 = sign_12;
            oldpos_7 = oldpos_6;
            strlen_16 = strlen_15;
            block = 28;
            break;
            case 28:
            v83 = (digit_0>=base_16);
            s_21 = s_20;
            base_17 = base_16;
            i_16 = i_15;
            digit_1 = digit_0;
            sign_14 = sign_13;
            oldpos_8 = oldpos_7;
            strlen_17 = strlen_16;
            v85 = val_12;
            if (v83 == false)
            {
                block = 29;
                break;
            }
            s_10 = s_20;
            val_1 = val_12;
            i_6 = i_15;
            sign_2 = sign_13;
            strlen_6 = strlen_16;
            v45 = oldpos_7;
            block = 13;
            break;
            case 29:
            v86 = (v85*base_17);
            v87 = (v86+digit_1);
            v88 = (i_16+1);
            s_9 = s_21;
            base_9 = base_17;
            val_0 = v87;
            i_5 = v88;
            sign_1 = sign_14;
            oldpos_0 = oldpos_8;
            strlen_5 = strlen_17;
            block = 12;
            break;
            case 30:
            v89 = (c_4<=90);
            s_23 = s_22;
            base_19 = base_18;
            c_5 = c_4;
            val_14 = val_13;
            i_18 = i_17;
            sign_16 = sign_15;
            oldpos_10 = oldpos_9;
            strlen_19 = strlen_18;
            v90 = v89;
            block = 31;
            break;
            case 31:
            s_16 = s_23;
            base_12 = base_19;
            c_1 = c_5;
            val_8 = val_14;
            i_11 = i_18;
            sign_9 = sign_16;
            oldpos_3 = oldpos_10;
            strlen_12 = strlen_19;
            if (v90 == false)
            {
                block = 24;
                break;
            }
            s_24 = s_23;
            base_20 = base_19;
            val_15 = val_14;
            i_19 = i_18;
            sign_17 = sign_16;
            oldpos_11 = oldpos_10;
            strlen_20 = strlen_19;
            v92 = c_5;
            block = 32;
            break;
            case 32:
            v93 = (v92-65);
            v94 = (v93+10);
            s_20 = s_24;
            base_16 = base_20;
            val_12 = val_15;
            i_15 = i_19;
            digit_0 = v94;
            sign_13 = sign_17;
            oldpos_7 = oldpos_11;
            strlen_16 = strlen_20;
            block = 28;
            break;
            case 33:
            v95 = (c_6<=122);
            s_26 = s_25;
            base_22 = base_21;
            c_7 = c_6;
            val_17 = val_16;
            i_21 = i_20;
            sign_19 = sign_18;
            oldpos_13 = oldpos_12;
            strlen_22 = strlen_21;
            v96 = v95;
            block = 34;
            break;
            case 34:
            s_15 = s_26;
            base_11 = base_22;
            c_0 = c_7;
            val_7 = val_17;
            i_10 = i_21;
            sign_8 = sign_19;
            oldpos_2 = oldpos_13;
            strlen_11 = strlen_22;
            if (v96 == false)
            {
                block = 23;
                break;
            }
            s_27 = s_26;
            base_23 = base_22;
            val_18 = val_17;
            i_22 = i_21;
            sign_20 = sign_19;
            oldpos_14 = oldpos_13;
            strlen_23 = strlen_22;
            v98 = c_7;
            block = 35;
            break;
            case 35:
            v99 = (v98-97);
            v100 = (v99+10);
            s_20 = s_27;
            base_16 = base_23;
            val_12 = val_18;
            i_15 = i_22;
            digit_0 = v100;
            sign_13 = sign_20;
            oldpos_7 = oldpos_14;
            strlen_16 = strlen_23;
            block = 28;
            break;
            case 36:
            v102 = s_28.charAt(i_23);
            v103 = (v102==' ');
            s_9 = s_28;
            base_9 = base_24;
            val_0 = 0;
            i_5 = i_23;
            sign_1 = sign_21;
            oldpos_0 = i_23;
            strlen_5 = strlen_24;
            if (v103 == false)
            {
                block = 12;
                break;
            }
            s_29 = s_28;
            base_25 = base_24;
            sign_22 = sign_21;
            strlen_25 = strlen_24;
            v105 = i_23;
            block = 37;
            break;
            case 37:
            v106 = (v105+1);
            s_8 = s_29;
            base_8 = base_25;
            i_4 = v106;
            sign_0 = sign_22;
            strlen_4 = strlen_25;
            block = 11;
            break;
            case 38:
            v108 = (v107+1);
            s_8 = s_30;
            base_8 = base_26;
            i_4 = v108;
            sign_0 = 1;
            strlen_4 = strlen_26;
            block = 11;
            break;
            case 39:
            v110 = (v109+1);
            s_8 = s_31;
            base_8 = base_27;
            i_4 = v110;
            sign_0 = -1;
            strlen_4 = strlen_27;
            block = 11;
            break;
            case 40:
            v112 = s_32.charAt(i_24);
            v113 = (v112==' ');
            s_5 = s_32;
            base_5 = base_28;
            i_1 = i_24;
            strlen_1 = strlen_28;
            if (v113 == false)
            {
                block = 7;
                break;
            }
            s_33 = s_32;
            base_29 = base_28;
            strlen_29 = strlen_28;
            v115 = i_24;
            block = 41;
            break;
            case 41:
            v116 = (v115+1);
            s_4 = s_33;
            base_4 = base_29;
            i_0 = v116;
            strlen_0 = strlen_29;
            block = 6;
            break;
            case 2:
            throw(evalue_0);
            case 18:
            return ( v15 );
        }
    }
}

function ll_null_item__List_Signed_ (lst_0) {
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            undefined;
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

function exceptions_StandardError () {
}

exceptions_StandardError.prototype.toString = function (){
    return ( '<exceptions.StandardError object>' );
}

inherits(exceptions_StandardError,exceptions_Exception);
function exceptions_ValueError () {
}

exceptions_ValueError.prototype.toString = function (){
    return ( '<exceptions.ValueError object>' );
}

inherits(exceptions_ValueError,exceptions_StandardError);
function State___init__ (self_0) {
    var v150;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v150 = new Array();
            v150.length = 0;
            self_0.ostack = v150;
            block = 1;
            break;
            case 1:
            return ( undefined );
        }
    }
}

function ll_striter__String (string_0) {
    var v153,v154;
    var block = 0;
    for(;;){
        switch(block){
            case 0:
            v154 = new Object();
            v154.string = string_0;
            v154.index = 0;
            v153 = v154;
            block = 1;
            break;
            case 1:
            return ( v153 );
        }
    }
}

function exceptions_StopIteration () {
}

exceptions_StopIteration.prototype.toString = function (){
    return ( '<exceptions.StopIteration object>' );
}

inherits(exceptions_StopIteration,exceptions_Exception);
function exceptions_Exception_meta () {
}

exceptions_Exception_meta.prototype.toString = function (){
    return ( '<exceptions.Exception_meta object>' );
}

inherits(exceptions_Exception_meta,Object_meta);
function exceptions_StandardError_meta () {
}

exceptions_StandardError_meta.prototype.toString = function (){
    return ( '<exceptions.StandardError_meta object>' );
}

inherits(exceptions_StandardError_meta,exceptions_Exception_meta);
function exceptions_StopIteration_meta () {
}

exceptions_StopIteration_meta.prototype.toString = function (){
    return ( '<exceptions.StopIteration_meta object>' );
}

inherits(exceptions_StopIteration_meta,exceptions_Exception_meta);
function exceptions_ValueError_meta () {
}

exceptions_ValueError_meta.prototype.toString = function (){
    return ( '<exceptions.ValueError_meta object>' );
}

inherits(exceptions_ValueError_meta,exceptions_StandardError_meta);
__consts_0 = {};
__consts_0.exceptions_ValueError__5 = exceptions_ValueError;
__consts_0.exceptions_ValueError_meta = new exceptions_ValueError_meta();
__consts_0.exceptions_ValueError = new exceptions_ValueError();
__consts_0.exceptions_StopIteration__7 = exceptions_StopIteration;
__consts_0.rpn_State = rpn_State;
__consts_0.rpn_State_meta = new rpn_State_meta();
__consts_0.exceptions_StopIteration_meta = new exceptions_StopIteration_meta();
__consts_0.exceptions_StopIteration = new exceptions_StopIteration();
__consts_0.const_list = undefined;
__consts_0.exceptions_ValueError_meta.class_ = __consts_0.exceptions_ValueError__5;
__consts_0.exceptions_ValueError.meta = __consts_0.exceptions_ValueError_meta;
__consts_0.rpn_State_meta.class_ = __consts_0.rpn_State;
__consts_0.exceptions_StopIteration_meta.class_ = __consts_0.exceptions_StopIteration__7;
__consts_0.exceptions_StopIteration.meta = __consts_0.exceptions_StopIteration_meta;
