#include <random>
#include "../box2d_wrapper.hpp"



struct b2EmitterDefBase
{
    b2EmitterDefBase();

    b2Body * body;
    b2Transform transform;
    float  emitRate;
    float lifetime;
    int seed;
    bool enabled;
};


struct b2RandomizedRadialEmitterDef : public b2EmitterDefBase
{
    b2RandomizedRadialEmitterDef();

    float innerRadius;
    float outerRadius;
    float velocityMagnitude;

    float startAngle;
    float stopAngle;
};


struct b2RandomizedLinearEmitterDef : public b2EmitterDefBase
{
    b2RandomizedLinearEmitterDef();

    b2Vec2 size;
    b2Vec2 velocity;
};

struct b2LinearEmitterArrayDef : public b2EmitterDefBase
{
    b2LinearEmitterArrayDef();

    std::size_t n_emitter;
    float length;
    b2Vec2 velocity;
};



class b2EmitterBase
{
public:
    b2EmitterBase(
        b2ParticleSystem * particleSystem,
        const b2EmitterDefBase & def
    );
    void CreateParticle(b2ParticleDef  def);
    b2Body* GetBody()const;
    void SetBody(b2Body * body);

    const b2Transform & GetTransform()const;
    void SetTransform(const b2Transform & transform);

    const b2Vec2 & GetPosition()const;
    void SetPosition(const b2Vec2 & vec);

    float GetAngle()const;
    void SetAngle(const float angle);

    bool GetEnabled()const;
    void SetEnabled(const bool e);

protected:


    b2ParticleSystem * m_particleSystem;

    b2Body * m_body;
    b2Transform m_transform;
    float  m_emitRate;
    float m_lifetime;
    int m_seed;
    bool m_enabled;
};



class b2RandomizedLinearEmitter: public b2EmitterBase {
public:
    b2RandomizedLinearEmitter(
        b2ParticleSystem * particleSystem,
        const b2RandomizedLinearEmitterDef & def
    );

    int Step(const float dt);

private:
    b2RandomizedLinearEmitterDef m_emmiter_def;
    float m_remainder;
    std::uniform_real_distribution<float> m_uniform01;
    std::mt19937 m_gen;
};


class b2LinearEmitterArray: public b2EmitterBase {
public:
    b2LinearEmitterArray(
        b2ParticleSystem * particleSystem,
        const b2LinearEmitterArrayDef & def
    );

    int Step(const float dt);

private:
    b2LinearEmitterArrayDef m_emmiter_def;
    float m_remainder;
};


class b2RandomizedRadialEmitter : b2EmitterBase
{
public:
    b2RandomizedRadialEmitter(
        b2ParticleSystem * particleSystem,
        const b2RandomizedRadialEmitterDef & def
    );

    int Step(const float dt);

private:
    b2RandomizedRadialEmitterDef m_emmiter_def;

    float m_remainder;
    std::uniform_real_distribution<float> m_uniform_r;
    std::uniform_real_distribution<float> m_uniform_angle;
    std::mt19937 m_gen;
};
