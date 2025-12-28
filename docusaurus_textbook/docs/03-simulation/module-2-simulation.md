---
title: "Module 2: Simulation & Digital Twins"
description: "Physics simulation, Gazebo, Unity, and building digital twins"
module: 2
duration: "8-12 hours"
prerequisites: "ROS 2 basics"
objectives:
  - Understand Gazebo and Unity for robot simulation
  - Build digital twins and simulate sensors
  - Prepare environments for sim-to-real transfer
---

<div style={{
  background: 'linear-gradient(135deg, #0891b2, #7c3aed)',
  padding: '50px 30px',
  borderRadius: '20px',
  marginBottom: '30px',
  color: 'white',
  boxShadow: '0 15px 50px rgba(8, 145, 178, 0.4)'
}}>
  <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '15px' }}>
    <span style={{ fontSize: '48px' }}>🌐</span>
    <div>
      <div style={{ fontSize: '14px', opacity: 0.9, textTransform: 'uppercase', letterSpacing: '2px' }}>Module 2</div>
      <h1 style={{ fontSize: '42px', margin: '5px 0', color: 'white' }}>Simulation & Digital Twins</h1>
    </div>
  </div>
  <p style={{ fontSize: '20px', lineHeight: '1.6', margin: '20px 0 0 0', maxWidth: '800px' }}>
    Build virtual worlds to test and train your humanoid robots before deploying to reality
  </p>
</div>

<div style={{
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
  gap: '15px',
  marginBottom: '30px'
}}>
  <div style={{
    background: 'linear-gradient(135deg, rgba(8, 145, 178, 0.1), rgba(124, 58, 237, 0.1))',
    padding: '25px',
    borderRadius: '12px',
    textAlign: 'center',
    border: '2px solid rgba(8, 145, 178, 0.2)'
  }}>
    <div style={{ fontSize: '36px', marginBottom: '10px' }}>⚙️</div>
    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0891b2' }}>Gazebo</div>
    <div style={{ fontSize: '13px', color: '#64748b' }}>Physics simulation</div>
  </div>
  <div style={{
    background: 'linear-gradient(135deg, rgba(8, 145, 178, 0.1), rgba(124, 58, 237, 0.1))',
    padding: '25px',
    borderRadius: '12px',
    textAlign: 'center',
    border: '2px solid rgba(8, 145, 178, 0.2)'
  }}>
    <div style={{ fontSize: '36px', marginBottom: '10px' }}>🎮</div>
    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0891b2' }}>Unity</div>
    <div style={{ fontSize: '13px', color: '#64748b' }}>Visual rendering</div>
  </div>
  <div style={{
    background: 'linear-gradient(135deg, rgba(8, 145, 178, 0.1), rgba(124, 58, 237, 0.1))',
    padding: '25px',
    borderRadius: '12px',
    textAlign: 'center',
    border: '2px solid rgba(8, 145, 178, 0.2)'
  }}>
    <div style={{ fontSize: '36px', marginBottom: '10px' }}>🔄</div>
    <div style={{ fontSize: '16px', fontWeight: 'bold', color: '#0891b2' }}>Sim2Real</div>
    <div style={{ fontSize: '13px', color: '#64748b' }}>Transfer learning</div>
  </div>
</div>

## 🚀 Bridge Between Design and Reality

Simulation is the bridge between design and reality. In this module you'll:
- Set up Gazebo and create SDF/URDF-based robots conceptually.
- Use Unity for high-fidelity rendering and interactive HRI testing.
- Simulate sensors: cameras, LiDAR, IMU, contact sensors.
- Plan datasets for synthetic data generation to train perception models.

## Learning Activities (static)
- Design a simulated environment checklist (lighting, textures, physics parameters).
- Create a dataset plan: object types, poses, lighting variations, annotation schema.
- Define sim-to-real transfer steps: domain randomization list, system ID parameters to record.
