// MIT License

// Copyright (c) 2019 Erin Catto

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#define _CRT_SECURE_NO_WARNINGS

#include "box2d/b2_settings.h"
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>

b2Version b2_version = {2, 4, 0};

#define LIQUIDFUN_VERSION_MAJOR 1
#define LIQUIDFUN_VERSION_MINOR 1
#define LIQUIDFUN_VERSION_REVISION 0
#define LIQUIDFUN_STRING_EXPAND(X) #X
#define LIQUIDFUN_STRING(X) LIQUIDFUN_STRING_EXPAND(X)

static void* b2AllocDefault(int32 size, void* callbackData);
static void b2FreeDefault(void* mem, void* callbackData);

const b2Version b2_liquidFunVersion = {
	LIQUIDFUN_VERSION_MAJOR, LIQUIDFUN_VERSION_MINOR,
	LIQUIDFUN_VERSION_REVISION,
};

const char *b2_liquidFunVersionString =
	"LiquidFun "
	LIQUIDFUN_STRING(LIQUIDFUN_VERSION_MAJOR) "."
	LIQUIDFUN_STRING(LIQUIDFUN_VERSION_MINOR) "."
	LIQUIDFUN_STRING(LIQUIDFUN_VERSION_REVISION);

static int32 b2_numAllocs = 0;

// Initialize default allocator.
static b2AllocFunction b2_allocCallback = b2AllocDefault;
static b2FreeFunction b2_freeCallback = b2FreeDefault;
static void *b2_callbackData = nullptr;

// Default implementation of b2AllocFunction.
static void* b2AllocDefault(int32 size, void* callbackData)
{
	B2_NOT_USED(callbackData);
	return malloc(size);
}

// Default implementation of b2FreeFunction.
static void b2FreeDefault(void* mem, void* callbackData)
{
	B2_NOT_USED(callbackData);
	free(mem);
}

/// Set alloc and free callbacks to override the default behavior of using
/// malloc() and free() for dynamic memory allocation.
/// Set allocCallback and freeCallback to nullptr to restore the default
/// allocator (malloc / free).
void b2SetAllocFreeCallbacks(b2AllocFunction allocCallback,
							 b2FreeFunction freeCallback, void* callbackData)
{
	b2Assert((allocCallback && freeCallback) ||
			 (!allocCallback && !freeCallback));
	b2Assert(0 == b2GetNumAllocs());
	if (allocCallback && freeCallback)
	{
		b2_allocCallback = allocCallback;
		b2_freeCallback = freeCallback;
		b2_callbackData = callbackData;
	}
	else
	{
		b2_allocCallback = b2AllocDefault;
		b2_freeCallback = b2FreeDefault;
		b2_callbackData = nullptr;
	}
}

// Memory allocators. Modify these to use your own allocator.
void* b2Alloc_Default(int32 size)
{
	b2_numAllocs++;
	return b2_allocCallback(size, b2_callbackData);
}

void b2Free_Default(void* mem)
{
	b2_numAllocs--;
	b2_freeCallback(mem, b2_callbackData);
}

void b2SetNumAllocs(const int32 numAllocs)
{
	b2_numAllocs = numAllocs;
}

int32 b2GetNumAllocs()
{
	return b2_numAllocs;
}

// You can modify this to use your logging facility.
void b2Log_Default(const char* string, va_list args)
{
#if DEBUG
	vprintf(string, args);
#else
	B2_NOT_USED(string);
	B2_NOT_USED(args);
#endif
}

FILE* b2_dumpFile = nullptr;

void b2OpenDump(const char* fileName)
{
	b2Assert(b2_dumpFile == nullptr);
	b2_dumpFile = fopen(fileName, "w");
}

void b2Dump(const char* string, ...)
{
	if (b2_dumpFile == nullptr)
	{
		return;
	}

	va_list args;
	va_start(args, string);
	vfprintf(b2_dumpFile, string, args);
	va_end(args);
}

void b2CloseDump()
{
	fclose(b2_dumpFile);
	b2_dumpFile = nullptr;
}

class Validator
{
public:
	Validator()
	{
		b2Assert(sizeof(uint64)==8);
		b2Assert(sizeof(int64)==8);
}
} validate;
