// MIT License

// Copyright (c) 2019 Erin Catto
// Copyright (c) 2014 Google, Inc.

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

#include "box2d/b2_timer.h"

#if defined(_WIN32)

double b2Timer::s_invFrequency = 0.0;

#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN
#endif

#include <windows.h>

typedef BOOL (WINAPI *SystemGetTimeFunc)(_Out_ LARGE_INTEGER *lpFrequency);
SystemGetTimeFunc systemGetTimeFunc = ::QueryPerformanceCounter;
SystemGetTimeFunc systemGetFreqFunc = ::QueryPerformanceFrequency;

int64 b2Timer::GetTicks()
{
	LARGE_INTEGER largeInteger;
	systemGetTimeFunc(&largeInteger);
	return largeInteger.QuadPart;
}

b2Timer::b2Timer()
{
	LARGE_INTEGER largeInteger;

	if (s_invFrequency == 0.0)
	{
		systemGetFreqFunc(&largeInteger);
		s_invFrequency = double(largeInteger.QuadPart);
		if (s_invFrequency > 0.0)
		{
			s_invFrequency = 1000.0 / s_invFrequency;
		}
	}

	m_start = GetTicks();
}

void b2Timer::Reset()
{
	m_start = GetTicks();
}

float b2Timer::GetMilliseconds() const
{
	int64 elapsed = GetTicks() - m_start;
	return (float)(s_invFrequency * elapsed);
}

#elif defined(__linux__) || defined (__APPLE__)

#include <sys/time.h>
#include <time.h>

// systemGetTimeFunc is defined with external linkage to allow unit
// test to mock out the system time function

#if defined(__linux__)

typedef int (*SystemGetTimeFunc)(clockid_t clk_id, struct timespec *tp);
SystemGetTimeFunc systemGetTimeFunc = ::clock_gettime;

#elif defined(__APPLE__)

typedef int (*SystemGetTimeFunc)(struct timeval * tp, void * tzp);
SystemGetTimeFunc systemGetTimeFunc = ::gettimeofday;

#endif

int64 b2Timer::GetTicks()
{
	static const int NSEC_PER_SEC = 1000000000;

#ifdef __linux__
	timespec ts;
	systemGetTimeFunc(CLOCK_MONOTONIC,&ts);
	return ((int64)ts.tv_sec) * NSEC_PER_SEC + ts.tv_nsec;
#else
	timeval t;
	systemGetTimeFunc(&t, 0);
	return ((int64)t.tv_sec) * NSEC_PER_SEC + t.tv_usec * 1000;
#endif
}

b2Timer::b2Timer()
{
    Reset();
}

void b2Timer::Reset()
{
    m_start = GetTicks();
}

float b2Timer::GetMilliseconds() const
{
  static const float kTicksToMs = 0.000001f;
	return kTicksToMs * (float)(GetTicks() - m_start);
}

#else

b2Timer::b2Timer()
{
}

void b2Timer::Reset()
{
}

float b2Timer::GetMilliseconds() const
{
	return 0.0f;
}

#endif
