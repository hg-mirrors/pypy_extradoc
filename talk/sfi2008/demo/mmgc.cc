		static const int NATIVE_COOKIE      = 0x10000000;
		/*@}*/

		DWB(Traits*) declaringTraits;
		DWB(Traits*) activationTraits;
		DWB(PoolObject*) pool;
		
		AvmCore* core() const
		{
			return pool->core;
		}

		uintptr iid() const
		{
			return ((uintptr)this)>>3;
		}
