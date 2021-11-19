/*
* Copyright (c) 2013 Google, Inc.
*
* This software is provided 'as-is', without any express or implied
* warranty.  In no event will the authors be held liable for any damages
* arising from the use of this software.
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
* 1. The origin of this software must not be misrepresented; you must not
* claim that you wrote the original software. If you use this software
* in a product, an acknowledgment in the product documentation would be
* appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
* misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*/
#ifndef B2_STAT
#define B2_STAT

#include "b2_api.h"

/// Calculates min/max/mean of a set of samples
class B2_API b2Stat
{
public:
	b2Stat();

	/// Record a sample
	void Record( float t );

	/// Returns the number of recorded samples
	int GetCount() const;

	/// Returns the mean of all recorded samples,
	/// Returns 0 if there are no recorded samples
	float GetMean() const;

	/// Returns the min of all recorded samples,
	/// FLT_MAX if there are no recorded samples
	float GetMin() const;

	/// Returns the max of all recorded samples,
	/// -FLT_MAX if there are no recorded samples
	float GetMax() const;

	/// Erase all recorded samples
	void Clear();
private:

	int m_count;
	double m_total;
	float m_min;
	float m_max;
};

#endif
