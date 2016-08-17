.class public pypy/interpret_35
.super java/lang/Object
.method public <init>()V
  ;      load_jvm_jar: jvartype=Class<Lpypy/interpret_35;> varidx=0
    .line 0
    aload_0                                                     
    .line 1
    invokespecial java/lang/Object/<init>()V                    
    .line 2
    return                                                      
.limit stack 100
.limit locals 1
.end method
.method public static invoke(Ljava/lang/String;I)I
  BasicBlock_16:
  ; v24 = new((<Instance(rpn.State)>))
    .line 1
    new pypy/rpn/State_36                                       
    .line 2
    dup                                                         
    .line 3
    invokespecial pypy/rpn/State_36/<init>()V                   
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=2
    .line 4
    astore_2                                                    
  ; v25 = oosetfield(v24, ('meta'), (<'Object_meta' view of...6726ec>))
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=2
    .line 5
    aload_2                                                     
    .line 6
    getstatic pypy/Constant/pypy_rpn_State_meta_38__37 Lpypy/rpn/State_meta_38;
    .line 7
    checkcast pypy/Object_meta_12                               
    .line 8
    putfield pypy/Object_10/meta Lpypy/Object_meta_12;          
  ; v26 = new((<List(Signed)>))
    .line 9
    new java/util/ArrayList                                     
    .line 10
    dup                                                         
    .line 11
    invokespecial java/util/ArrayList/<init>()V                 
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=3
    .line 12
    astore_3                                                    
  ; v27 = oosend(('_ll_resize'), v26, (0))
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=3
    .line 13
    aload_3                                                     
    .line 14
    iconst_0                                                    
    .line 15
    invokestatic pypy/PyPy/_ll_resize(Ljava/util/ArrayList;I)V  
  ; v28 = oosetfield(v24, ('ostack'), v26)
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=2
    .line 16
    aload_2                                                     
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=3
    .line 17
    aload_3                                                     
    .line 18
    putfield pypy/rpn/State_36/ostack Ljava/util/ArrayList;     
  ; v29 = oogetfield(v24, ('ostack'))
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=2
    .line 19
    aload_2                                                     
    .line 20
    getfield pypy/rpn/State_36/ostack Ljava/util/ArrayList;     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=4
    .line 21
    astore 4                                                    
  ; v30 = oosend(('ll_length'), v29)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=4
    .line 22
    aload 4                                                     
    .line 23
    invokevirtual java/util/ArrayList/size()I                   
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=5
    .line 24
    istore 5                                                    
  ; v31 = int_add(v30, (1))
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=5
    .line 25
    iload 5                                                     
    .line 26
    iconst_1                                                    
    .line 27
    iadd                                                        
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=6
    .line 28
    istore 6                                                    
  ; v32 = oosend(('_ll_resize_ge'), v29, v31)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=4
    .line 29
    aload 4                                                     
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=6
    .line 30
    iload 6                                                     
    .line 31
    invokestatic pypy/PyPy/_ll_resize_ge(Ljava/util/ArrayList;I)V
  ; v33 = oosend(('ll_setitem_fast'), v29, v30, arg_0)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=4
    .line 32
    aload 4                                                     
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=5
    .line 33
    iload 5                                                     
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=1
    .line 34
    iload_1                                                     
    .line 35
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    .line 36
    invokestatic pypy/PyPy/ll_setitem_fast(Ljava/util/ArrayList;ILjava/lang/Object;)V
  ; (0) --> v34
    .line 37
    iconst_0                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=7
    .line 38
    istore 7                                                    
  ; code_0 --> v35
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=0
    .line 39
    aload_0                                                     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 40
    astore 8                                                    
  ; v24 --> state_0
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=2
    .line 41
    aload_2                                                     
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 42
    astore 9                                                    
    .line 43
    goto BasicBlock_17                                          
  BasicBlock_17:
  ; v36 = oosend(('ll_strlen'), v35)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 45
    aload 8                                                     
    .line 46
    invokevirtual java/lang/String/length()I                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=10
    .line 47
    istore 10                                                   
  ; v37 = int_ge(v34, v36)
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=7
    .line 48
    iload 7                                                     
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=10
    .line 49
    iload 10                                                    
    .line 50
    if_icmpge cmpop_18                                          
    .line 51
    iconst_0                                                    
    .line 52
    goto cmpop_19                                               
  cmpop_18:
    .line 54
    iconst_1                                                    
  cmpop_19:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=11
    .line 56
    istore 11                                                   
  ; v35 --> v38
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 57
    aload 8                                                     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=12
    .line 58
    astore 12                                                   
  ; v34 --> index_0
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=7
    .line 59
    iload 7                                                     
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=13
    .line 60
    istore 13                                                   
  ; v35 --> string_0
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 61
    aload 8                                                     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=14
    .line 62
    astore 14                                                   
  ; state_0 --> state_1
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 63
    aload 9                                                     
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=15
    .line 64
    astore 15                                                   
  ;      load_jvm_jar: jvartype=JvmScalarType<Z> varidx=11
    .line 65
    iload 11                                                    
    .line 66
    ifeq BasicBlock_20                                          
  ; state_0 --> state_2
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 67
    aload 9                                                     
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=16
    .line 68
    astore 16                                                   
    .line 69
    goto BasicBlock_21                                          
  BasicBlock_20:
  ; v39 = int_add(index_0, (1))
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=13
    .line 71
    iload 13                                                    
    .line 72
    iconst_1                                                    
    .line 73
    iadd                                                        
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=17
    .line 74
    istore 17                                                   
  ; v40 = oosend(('ll_stritem_nonneg'), string_0, index_0)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=14
    .line 75
    aload 14                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=13
    .line 76
    iload 13                                                    
    .line 77
    invokevirtual java/lang/String/charAt(I)C                   
  ;      store_jvm_jar: vartype=JvmScalarType<C> varidx=18
    .line 78
    istore 18                                                   
  ; v41 = char_le(('0'), v40)
    .line 79
    ldc 48                                                      
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=18
    .line 80
    iload 18                                                    
    .line 81
    if_icmple cmpop_22                                          
    .line 82
    iconst_0                                                    
    .line 83
    goto cmpop_23                                               
  cmpop_22:
    .line 85
    iconst_1                                                    
  cmpop_23:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=19
    .line 87
    istore 19                                                   
  ; state_1 --> state_3
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=15
    .line 88
    aload 15                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=20
    .line 89
    astore 20                                                   
  ; v39 --> v42
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=17
    .line 90
    iload 17                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=21
    .line 91
    istore 21                                                   
  ; v38 --> v43
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=12
    .line 92
    aload 12                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=22
    .line 93
    astore 22                                                   
  ; v40 --> v44
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=18
    .line 94
    iload 18                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<C> varidx=23
    .line 95
    istore 23                                                   
  ;      load_jvm_jar: jvartype=JvmScalarType<Z> varidx=19
    .line 96
    iload 19                                                    
    .line 97
    ifeq BasicBlock_24                                          
  ; v40 --> c_0
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=18
    .line 98
    iload 18                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<C> varidx=24
    .line 99
    istore 24                                                   
  ; state_1 --> state_4
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=15
    .line 100
    aload 15                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=25
    .line 101
    astore 25                                                   
  ; v39 --> v45
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=17
    .line 102
    iload 17                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=26
    .line 103
    istore 26                                                   
  ; v38 --> v46
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=12
    .line 104
    aload 12                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=27
    .line 105
    astore 27                                                   
    .line 106
    goto BasicBlock_25                                          
  BasicBlock_24:
  ; v47 = char_eq(v44, ('+'))
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=23
    .line 108
    iload 23                                                    
    .line 109
    ldc 43                                                      
    .line 110
    if_icmpeq cmpop_26                                          
    .line 111
    iconst_0                                                    
    .line 112
    goto cmpop_27                                               
  cmpop_26:
    .line 114
    iconst_1                                                    
  cmpop_27:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=28
    .line 116
    istore 28                                                   
  ; v42 --> v34
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=21
    .line 117
    iload 21                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=7
    .line 118
    istore 7                                                    
  ; v43 --> v35
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=22
    .line 119
    aload 22                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 120
    astore 8                                                    
  ; state_3 --> state_0
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=20
    .line 121
    aload 20                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 122
    astore 9                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<Z> varidx=28
    .line 123
    iload 28                                                    
    .line 124
    ifeq BasicBlock_17                                          
  ; state_3 --> state_5
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=20
    .line 125
    aload 20                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=29
    .line 126
    astore 29                                                   
  ; v42 --> v48
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=21
    .line 127
    iload 21                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=30
    .line 128
    istore 30                                                   
  ; v43 --> v49
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=22
    .line 129
    aload 22                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=31
    .line 130
    astore 31                                                   
    .line 131
    goto BasicBlock_28                                          
  BasicBlock_28:
  ; v50 = oosend(('oadd'), state_5)
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=29
    .line 133
    aload 29                                                    
    .line 134
    invokevirtual pypy/rpn/State_36/oadd()V                     
  ; v48 --> v34
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=30
    .line 135
    iload 30                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=7
    .line 136
    istore 7                                                    
  ; v49 --> v35
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=31
    .line 137
    aload 31                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 138
    astore 8                                                    
  ; state_5 --> state_0
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=29
    .line 139
    aload 29                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 140
    astore 9                                                    
    .line 141
    goto BasicBlock_17                                          
  BasicBlock_25:
  ; v51 = char_le(c_0, ('9'))
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=24
    .line 143
    iload 24                                                    
    .line 144
    ldc 57                                                      
    .line 145
    if_icmple cmpop_29                                          
    .line 146
    iconst_0                                                    
    .line 147
    goto cmpop_30                                               
  cmpop_29:
    .line 149
    iconst_1                                                    
  cmpop_30:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=32
    .line 151
    istore 32                                                   
  ; state_4 --> state_3
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=25
    .line 152
    aload 25                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=20
    .line 153
    astore 20                                                   
  ; v45 --> v42
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=26
    .line 154
    iload 26                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=21
    .line 155
    istore 21                                                   
  ; v46 --> v43
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=27
    .line 156
    aload 27                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=22
    .line 157
    astore 22                                                   
  ; c_0 --> v44
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=24
    .line 158
    iload 24                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<C> varidx=23
    .line 159
    istore 23                                                   
  ;      load_jvm_jar: jvartype=JvmScalarType<Z> varidx=32
    .line 160
    iload 32                                                    
    .line 161
    ifeq BasicBlock_24                                          
  ; c_0 --> c_1
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=24
    .line 162
    iload 24                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<C> varidx=33
    .line 163
    istore 33                                                   
  ; state_4 --> state_6
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=25
    .line 164
    aload 25                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=34
    .line 165
    astore 34                                                   
  ; v45 --> v52
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=26
    .line 166
    iload 26                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=35
    .line 167
    istore 35                                                   
  ; v46 --> v53
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=27
    .line 168
    aload 27                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=36
    .line 169
    astore 36                                                   
    .line 170
    goto BasicBlock_31                                          
  BasicBlock_31:
  ; v54 = cast_char_to_int(c_1)
  ;      load_jvm_jar: jvartype=JvmScalarType<C> varidx=33
    .line 172
    iload 33                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=37
    .line 173
    istore 37                                                   
  ; v55 = int_sub(v54, (48))
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=37
    .line 174
    iload 37                                                    
    .line 175
    ldc 48                                                      
    .line 176
    isub                                                        
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=38
    .line 177
    istore 38                                                   
  ; v56 = oogetfield(state_6, ('ostack'))
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=34
    .line 178
    aload 34                                                    
    .line 179
    getfield pypy/rpn/State_36/ostack Ljava/util/ArrayList;     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=39
    .line 180
    astore 39                                                   
  ; v57 = oosend(('ll_length'), v56)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=39
    .line 181
    aload 39                                                    
    .line 182
    invokevirtual java/util/ArrayList/size()I                   
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=40
    .line 183
    istore 40                                                   
  ; v58 = int_add(v57, (1))
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=40
    .line 184
    iload 40                                                    
    .line 185
    iconst_1                                                    
    .line 186
    iadd                                                        
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=41
    .line 187
    istore 41                                                   
  ; v59 = oosend(('_ll_resize_ge'), v56, v58)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=39
    .line 188
    aload 39                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=41
    .line 189
    iload 41                                                    
    .line 190
    invokestatic pypy/PyPy/_ll_resize_ge(Ljava/util/ArrayList;I)V
  ; v60 = oosend(('ll_setitem_fast'), v56, v57, v55)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=39
    .line 191
    aload 39                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=40
    .line 192
    iload 40                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=38
    .line 193
    iload 38                                                    
    .line 194
    invokestatic java/lang/Integer/valueOf(I)Ljava/lang/Integer;
    .line 195
    invokestatic pypy/PyPy/ll_setitem_fast(Ljava/util/ArrayList;ILjava/lang/Object;)V
  ; v52 --> v34
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=35
    .line 196
    iload 35                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=7
    .line 197
    istore 7                                                    
  ; v53 --> v35
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/lang/String;> varidx=36
    .line 198
    aload 36                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/lang/String;> varidx=8
    .line 199
    astore 8                                                    
  ; state_6 --> state_0
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=34
    .line 200
    aload 34                                                    
  ;      store_jvm_jar: vartype=Class<Lpypy/rpn/State_36;> varidx=9
    .line 201
    astore 9                                                    
    .line 202
    goto BasicBlock_17                                          
  BasicBlock_21:
  ; v61 = oogetfield(state_2, ('ostack'))
  ;      load_jvm_jar: jvartype=Class<Lpypy/rpn/State_36;> varidx=16
    .line 204
    aload 16                                                    
    .line 205
    getfield pypy/rpn/State_36/ostack Ljava/util/ArrayList;     
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=42
    .line 206
    astore 42                                                   
  ; v62 = oosend(('ll_length'), v61)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=42
    .line 207
    aload 42                                                    
    .line 208
    invokevirtual java/util/ArrayList/size()I                   
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=43
    .line 209
    istore 43                                                   
  ; v63 = int_lt((-1), (0))
    .line 210
    iconst_m1                                                   
    .line 211
    iconst_0                                                    
    .line 212
    if_icmplt cmpop_32                                          
    .line 213
    iconst_0                                                    
    .line 214
    goto cmpop_33                                               
  cmpop_32:
    .line 216
    iconst_1                                                    
  cmpop_33:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=44
    .line 218
    istore 44                                                   
  ; v61 --> l_0
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=42
    .line 219
    aload 42                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=45
    .line 220
    astore 45                                                   
  ; (-1) --> index_1
    .line 221
    iconst_m1                                                   
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=46
    .line 222
    istore 46                                                   
  ; v62 --> length_0
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=43
    .line 223
    iload 43                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=47
    .line 224
    istore 47                                                   
  ;      load_jvm_jar: jvartype=JvmScalarType<Z> varidx=44
    .line 225
    iload 44                                                    
    .line 226
    ifeq BasicBlock_34                                          
  ; v61 --> l_1
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=42
    .line 227
    aload 42                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=48
    .line 228
    astore 48                                                   
  ; v62 --> length_1
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=43
    .line 229
    iload 43                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=49
    .line 230
    istore 49                                                   
  ; (-1) --> v64
    .line 231
    iconst_m1                                                   
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=50
    .line 232
    istore 50                                                   
    .line 233
    goto BasicBlock_35                                          
  BasicBlock_34:
  ; v65 = int_ge(index_1, (0))
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=46
    .line 235
    iload 46                                                    
    .line 236
    iconst_0                                                    
    .line 237
    if_icmpge cmpop_36                                          
    .line 238
    iconst_0                                                    
    .line 239
    goto cmpop_37                                               
  cmpop_36:
    .line 241
    iconst_1                                                    
  cmpop_37:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=51
    .line 243
    istore 51                                                   
  ; v66 = debug_assert(v65, ('negative list getitem index out of bound'))
  ; v67 = int_lt(index_1, length_0)
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=46
    .line 244
    iload 46                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=47
    .line 245
    iload 47                                                    
    .line 246
    if_icmplt cmpop_38                                          
    .line 247
    iconst_0                                                    
    .line 248
    goto cmpop_39                                               
  cmpop_38:
    .line 250
    iconst_1                                                    
  cmpop_39:
  ;      store_jvm_jar: vartype=JvmScalarType<Z> varidx=52
    .line 252
    istore 52                                                   
  ; v68 = debug_assert(v67, ('list getitem index out of bound'))
  ; v69 = oosend(('ll_getitem_fast'), l_0, index_1)
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=45
    .line 253
    aload 45                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=46
    .line 254
    iload 46                                                    
    .line 255
    invokevirtual java/util/ArrayList/get(I)Ljava/lang/Object;  
    .line 256
    checkcast java/lang/Integer                                 
    .line 257
    invokevirtual java/lang/Integer/intValue()I                 
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=53
    .line 258
    istore 53                                                   
  ; v69 --> v70
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=53
    .line 259
    iload 53                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=54
    .line 260
    istore 54                                                   
    .line 261
    goto BasicBlock_40                                          
  BasicBlock_35:
  ; v71 = int_add(v64, length_1)
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=50
    .line 263
    iload 50                                                    
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=49
    .line 264
    iload 49                                                    
    .line 265
    iadd                                                        
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=55
    .line 266
    istore 55                                                   
  ; l_1 --> l_0
  ;      load_jvm_jar: jvartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=48
    .line 267
    aload 48                                                    
  ;      store_jvm_jar: vartype=JvmBuiltInType<Ljava/util/ArrayList;> varidx=45
    .line 268
    astore 45                                                   
  ; v71 --> index_1
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=55
    .line 269
    iload 55                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=46
    .line 270
    istore 46                                                   
  ; length_1 --> length_0
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=49
    .line 271
    iload 49                                                    
  ;      store_jvm_jar: vartype=JvmScalarType<I> varidx=47
    .line 272
    istore 47                                                   
    .line 273
    goto BasicBlock_34                                          
  BasicBlock_40:
  ;      load_jvm_jar: jvartype=JvmScalarType<I> varidx=54
    .line 275
    iload 54                                                    
    .line 276
    ireturn                                                     
.limit stack 100
.limit locals 56
.end method
