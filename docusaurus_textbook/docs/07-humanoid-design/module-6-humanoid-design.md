---
title: "Module 6: Designing Humanoid Robots"
description: "Kinematics, dynamics, URDF/Xacro, bipedal locomotion, hands and manipulation"
module: 6
duration: "8-12 hours"
prerequisites: "Mechanics basics, ROS 2"
objectives:
  - Model humanoid kinematics in URDF/Xacro (conceptual)
  - Understand dynamic stability, ZMP, and gait cycles
  - Design manipulators and end-effector control
---

<div style={{
  background: 'linear-gradient(135deg, #059669, #0891b2)',
  padding: '50px 30px',
  borderRadius: '20px',
  marginBottom: '30px',
  color: 'white',
  boxShadow: '0 15px 50px rgba(5, 150, 105, 0.4)'
}}>
  <div style={{ display: 'flex', alignItems: 'center', gap: '15px', marginBottom: '15px' }}>
    <span style={{ fontSize: '48px' }}>🤖</span>
    <div>
      <div style={{ fontSize: '14px', opacity: 0.9, textTransform: 'uppercase', letterSpacing: '2px' }}>Module 6 - Capstone</div>
      <h1 style={{ fontSize: '42px', margin: '5px 0', color: 'white' }}>Designing Humanoid Robots</h1>
    </div>
  </div>
  <p style={{ fontSize: '20px', lineHeight: '1.6', margin: '20px 0 0 0', maxWidth: '800px' }}>
    From mechanical design to bipedal locomotion - build complete humanoid systems
  </p>
</div>

<div style={{
  background: 'linear-gradient(135deg, rgba(5, 150, 105, 0.08), rgba(8, 145, 178, 0.08))',
  padding: '25px',
  borderRadius: '15px',
  marginBottom: '30px',
  border: '2px solid rgba(5, 150, 105, 0.2)'
}}>
  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px' }}>
    <div>
      <div style={{ fontSize: '12px', color: '#059669', fontWeight: 'bold', marginBottom: '5px' }}>⏱️ DURATION</div>
      <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#0891b2' }}>8-12 hours</div>
    </div>
    <div>
      <div style={{ fontSize: '12px', color: '#059669', fontWeight: 'bold', marginBottom: '5px' }}>📐 COMPLEXITY</div>
      <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#0891b2' }}>Advanced</div>
    </div>
    <div>
      <div style={{ fontSize: '12px', color: '#059669', fontWeight: 'bold', marginBottom: '5px' }}>🎓 TYPE</div>
      <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#0891b2' }}>Design & Build</div>
    </div>
  </div>
</div>

## 📐 Topics Covered
- URDF/Xacro design patterns (modularity, reusability).
- Kinematics overview: forward/inverse, joint chains and task spaces.
- Dynamics and stability: ZMP, CoM, gait generation concepts.
- Hands & manipulation: grasp taxonomy, compliance, sensor integration.

## Lab & Deliverables (static)
- Provide a design checklist for a humanoid limb (links to references in Appendix).
- Produce a gait analysis plan describing step timing, foot placement, and stability margins.
