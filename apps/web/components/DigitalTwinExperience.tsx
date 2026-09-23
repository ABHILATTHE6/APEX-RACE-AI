"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";
import { Canvas, useFrame } from "@react-three/fiber";
import { Line, OrbitControls } from "@react-three/drei";

type TelemetryPoint = {
  t: number;
  speed: number;
  rpm: number;
  gear: number;
  throttle: number;
  brake: number;
};

const telemetry: TelemetryPoint[] = Array.from({ length: 241 }, (_, index) => {
  const t = index / 240;
  const corner = Math.abs(Math.sin(t * Math.PI * 8));
  const speed = Math.round(182 + 118 * (1 - corner ** 3));
  return {
    t,
    speed,
    rpm: Math.round(7600 + speed * 13 + 350 * Math.sin(t * Math.PI * 16)),
    gear: Math.max(2, Math.min(8, Math.round((speed - 120) / 28))),
    throttle: Math.round(Math.max(0, Math.min(100, 96 - corner * 92))),
    brake: Math.round(Math.max(0, Math.min(100, corner * 82 - 6))),
  };
});

function TrackScene({ progress }: { progress: number }) {
  const carRef = useRef<THREE.Group>(null);
  const curve = useMemo(
    () =>
      new THREE.CatmullRomCurve3(
        [
          new THREE.Vector3(-18, 0, -9),
          new THREE.Vector3(-11, 0, -16),
          new THREE.Vector3(1, 0, -14),
          new THREE.Vector3(16, 0, -7),
          new THREE.Vector3(19, 0, 4),
          new THREE.Vector3(11, 0, 14),
          new THREE.Vector3(-2, 0, 16),
          new THREE.Vector3(-15, 0, 10),
          new THREE.Vector3(-19, 0, 1),
        ],
        true,
        "catmullrom",
        0.18,
      ),
    [],
  );

  const trackPoints = useMemo(
    () => curve.getPoints(220).map((point) => [point.x, point.y, point.z] as [number, number, number]),
    [curve],
  );

  useEffect(() => {
    if (!carRef.current) return;
    const point = curve.getPointAt(progress);
    const ahead = curve.getPointAt((progress + 0.006) % 1);
    carRef.current.position.copy(point);
    carRef.current.lookAt(ahead.x, point.y, ahead.z);
    carRef.current.rotateY(Math.PI);
  }, [curve, progress]);

  useFrame((_, delta) => {
    if (!carRef.current) return;
    carRef.current.position.y = 0.48 + Math.sin(performance.now() * 0.006) * 0.015;
  });

  return (
    <>
      <ambientLight intensity={2.1} />
      <directionalLight position={[12, 18, 6]} intensity={3.2} />
      <directionalLight position={[-14, 8, -12]} intensity={1.1} />

      <mesh rotation-x={-Math.PI / 2} position={[0, -0.25, 0]}>
        <planeGeometry args={[70, 58]} />
        <meshStandardMaterial color="#f1f1ef" roughness={1} />
      </mesh>

      <Line points={trackPoints} color="#222222" lineWidth={10} />
      <Line points={trackPoints} color="#dedede" lineWidth={4.5} />

      {Array.from({ length: 12 }, (_, index) => {
        const p = curve.getPointAt(index / 12);
        return (
          <mesh key={index} position={[p.x, 0.02, p.z]} rotation-x={-Math.PI / 2}>
            <planeGeometry args={[0.9, 0.9]} />
            <meshBasicMaterial color="#e11d2e" transparent opacity={0.75} />
          </mesh>
        );
      })}

      <group ref={carRef} position={[0, 0.48, 0]}>
        <mesh castShadow>
          <boxGeometry args={[2.3, 0.32, 4.4]} />
          <meshStandardMaterial color="#151515" metalness={0.55} roughness={0.35} />
        </mesh>
        <mesh position={[0, 0.18, -0.65]}>
          <boxGeometry args={[1.1, 0.18, 1.65]} />
          <meshStandardMaterial color="#292929" metalness={0.2} roughness={0.25} />
        </mesh>
        <mesh position={[0, 0.02, 1.55]}>
          <boxGeometry args={[2.7, 0.12, 0.48]} />
          <meshStandardMaterial color="#e11d2e" roughness={0.4} />
        </mesh>
        <mesh position={[0, 0.01, -1.85]}>
          <boxGeometry args={[2.6, 0.12, 0.42]} />
          <meshStandardMaterial color="#e11d2e" roughness={0.4} />
        </mesh>
        {[
          [-1.18, -0.62],
          [1.18, -0.62],
          [-1.18, 1.02],
          [1.18, 1.02],
        ].map(([x, z]) => (
          <mesh key={`${x}-${z}`} position={[x, -0.17, z]} rotation-z={Math.PI / 2}>
            <cylinderGeometry args={[0.42, 0.42, 0.24, 20]} />
            <meshStandardMaterial color="#191919" roughness={0.9} />
          </mesh>
        ))}
      </group>

      <OrbitControls enablePan={false} minDistance={25} maxDistance={48} target={[0, 0, 0]} />
    </>
  );
}

function Metric({ label, value, unit }: { label: string; value: string; unit?: string }) {
  return (
    <div className="metric">
      <small>{label}</small>
      <strong>{value} <em>{unit}</em></strong>
    </div>
  );
}

export default function DigitalTwinExperience() {
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const [mode, setMode] = useState("Speed");

  useEffect(() => {
    if (!playing) return;
    let frame = 0;
    const tick = () => {
      setProgress((current) => {
        const next = current + 0.0019;
        if (next >= 1) {
          setPlaying(false);
          return 0;
        }
        return next;
      });
      frame = requestAnimationFrame(tick);
    };
    frame = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(frame);
  }, [playing]);

  const sampleIndex = Math.min(telemetry.length - 1, Math.round(progress * (telemetry.length - 1)));
  const sample = telemetry[sampleIndex];

  const insight =
    sample.brake > 48
      ? "Observed heavy braking phase. Car is transitioning into a low-speed corner."
      : sample.throttle < 55
        ? "Observed partial throttle application through the current track segment."
        : "Observed high-throttle acceleration phase on the selected replay trace.";

  return (
    <main className="apex-shell">
      <header className="apex-header">
        <div>
          <div className="apex-brand">APEX-RACE <span>// AI</span></div>
          <div className="apex-subtitle">Real-time motorsport intelligence · digital twin workspace</div>
        </div>
        <div className="source-chip">SIMULATED PUBLIC-TELEMETRY DEMO</div>
      </header>

      <section className="hero-grid">
        <div className="panel canvas-panel">
          <div className="panel-head">
            <div className="kicker">Digital Twin</div>
            <div className="title">Monza-style circuit · telemetry-driven vehicle motion</div>
          </div>
          <div className="canvas-wrap">
            <Canvas camera={{ position: [29, 21, 28], fov: 42 }} dpr={[1, 1.6]}>
              <TrackScene progress={progress} />
            </Canvas>
          </div>
          <div className="canvas-overlay">
            <span className="legend-chip">CAR · LAP REPLAY</span>
            <span className="legend-chip">TRACK · 3D PROCEDURAL</span>
            <span className="legend-chip">DATA · SIMULATED</span>
          </div>
        </div>

        <aside className="panel side-panel">
          <div className="selector">
            <div className="field"><label>Event</label><strong>Italian Grand Prix</strong></div>
            <div className="field"><label>Session</label><strong>Qualifying</strong></div>
            <div className="field"><label>Driver</label><strong>LEC · Demo</strong></div>
            <div className="field"><label>Lap</label><strong>Fastest · 01</strong></div>
          </div>

          <div className="metrics">
            <Metric label="Speed" value={sample.speed.toString()} unit="km/h" />
            <Metric label="RPM" value={sample.rpm.toLocaleString()} unit="" />
            <Metric label="Gear" value={sample.gear.toString()} unit="" />
            <Metric label="Throttle" value={sample.throttle.toString()} unit="%" />
            <Metric label="Brake" value={sample.brake.toString()} unit="%" />
            <Metric label="Lap progress" value={Math.round(progress * 100).toString()} unit="%" />
          </div>

          <div className="timeline">
            <div className="controls">
              <button className="button primary" onClick={() => setPlaying((value) => !value)}>
                {playing ? "Pause" : "Play"}
              </button>
              <button className="button" onClick={() => setProgress(0)}>Reset</button>
              <select
                aria-label="Heatmap metric"
                className="button"
                value={mode}
                onChange={(event) => setMode(event.target.value)}
              >
                <option>Speed</option>
                <option>Throttle</option>
                <option>Brake</option>
                <option>Gear</option>
              </select>
            </div>
            <input
              className="range"
              type="range"
              min={0}
              max={1}
              step={0.001}
              value={progress}
              onChange={(event) => setProgress(Number(event.target.value))}
              aria-label="Replay timeline"
            />
            <div className="timeline-row">
              <span>00:00.000</span>
              <span>{Math.round(progress * 100)}% · {mode} layer</span>
              <span>01:19.842</span>
            </div>
          </div>

          <div className="insight">
            <strong>TRACK INSIGHT</strong>
            <p>{insight}</p>
            <div className="delta">Current telemetry: {sample.speed} km/h · {sample.throttle}% throttle · {sample.brake}% brake</div>
          </div>
        </aside>
      </section>
    </main>
  );
}
