// MIT License

// Copyright (c) 2019 Erin Catto
// Copyright (c) 2013 Google, Inc.

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

#ifndef B2_EDGE_SHAPE_H
#define B2_EDGE_SHAPE_H

#include "b2_api.h"
#include "b2_shape.h"

/// A line segment (edge) shape. These can be connected in chains or loops
/// to other edge shapes. Edges created independently are two-sided and do
/// no provide smooth movement across junctions.
class B2_API b2EdgeShape : public b2Shape
{
public:
	b2EdgeShape();

	/// Set this as a part of a sequence. Vertex v0 precedes the edge and vertex v3
	/// follows. These extra vertices are used to provide smooth movement
	/// across junctions. This also makes the collision one-sided. The edge
	/// normal points to the right looking from v1 to v2.
	void SetOneSided(const b2Vec2& v0, const b2Vec2& v1,const b2Vec2& v2, const b2Vec2& v3);

	/// Set this as an isolated edge. Collision is two-sided.
	void SetTwoSided(const b2Vec2& v1, const b2Vec2& v2);

	/// Implement b2Shape.
	b2Shape* Clone(b2BlockAllocator* allocator) const override;

	/// @see b2Shape::GetChildCount
	int32 GetChildCount() const override;

	/// @see b2Shape::TestPoint
	bool TestPoint(const b2Transform& transform, const b2Vec2& p) const override;

	// @see b2Shape::ComputeDistance
	void ComputeDistance(const b2Transform& xf, const b2Vec2& p, float* distance, b2Vec2* normal, int32 childIndex) const override;

	/// Implement b2Shape.
	bool RayCast(b2RayCastOutput* output, const b2RayCastInput& input,
				const b2Transform& transform, int32 childIndex) const override;

	/// @see b2Shape::ComputeAABB
	void ComputeAABB(b2AABB* aabb, const b2Transform& transform, int32 childIndex) const override;

	/// @see b2Shape::ComputeMass
	void ComputeMass(b2MassData* massData, float density) const override;

#if LIQUIDFUN_EXTERNAL_LANGUAGE_API
	/// Set this as an isolated edge, with direct floats.
	void Set(float vx1, float vy1, float vx2, float vy2);
#endif // LIQUIDFUN_EXTERNAL_LANGUAGE_API

	/// These are the edge vertices
	b2Vec2 m_vertex1, m_vertex2;

	/// Optional adjacent vertices. These are used for smooth collision.
	b2Vec2 m_vertex0, m_vertex3;

	/// Uses m_vertex0 and m_vertex3 to create smooth collision.
	bool m_oneSided;
};

inline b2EdgeShape::b2EdgeShape()
{
	m_type = e_edge;
	m_radius = b2_polygonRadius;
	m_vertex0.x = 0.0f;
	m_vertex0.y = 0.0f;
	m_vertex3.x = 0.0f;
	m_vertex3.y = 0.0f;
	m_oneSided = false;
}

#if LIQUIDFUN_EXTERNAL_LANGUAGE_API
inline void b2EdgeShape::Set(float vx1,
														 float vy1,
														 float vx2,
														 float vy2) {
	Set(b2Vec2(vx1, vy1), b2Vec2(vx2, vy2));
}
#endif // LIQUIDFUN_EXTERNAL_LANGUAGE_API


#endif
