
"use client"

import { useState, useEffect, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import clsx from 'clsx';
import { Camera, Moon, Sun, AlertCircle, Wifi, WifiOff, Volume2, VolumeX, Activity, Eye } from 'lucide-react';

// import * as tf from '@tensorflow/tfjs';
// import * as faceLandmarksDetection from '@tensorflow-models/face-landmarks-detection';
// import '@tensorflow/tfjs-backend-webgl';

// Mesh Keypoints for Eyes (MediaPipe Face Mesh)
const LEFT_EYE = [33, 160, 158, 133, 153, 144];
const RIGHT_EYE = [362, 385, 387, 263, 373, 380];

const EAR_THRESHOLD = 0.25;
const EAR_FRAMES = 10;

export default function Home() {
    const webcamRef = useRef<Webcam>(null);
    const requestRef = useRef<number | null>(null);
    const [model, setModel] = useState<any>(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const [alarm, setAlarm] = useState(false);
    const [ear, setEar] = useState<number>(0);
    const [isOnline, setIsOnline] = useState(true);
    const [mode, setMode] = useState<"day" | "night">("night");
    const [loading, setLoading] = useState(true);
    const [soundEnabled, setSoundEnabled] = useState(true);

    // Sound Synth
    const playAlarm = useCallback(() => {
        if (!soundEnabled) return;
        const ctx = new (window.AudioContext || (window as any).webkitAudioContext)();
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.type = 'sawtooth';
        oscillator.frequency.setValueAtTime(800, ctx.currentTime);
        oscillator.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.1);
        gainNode.gain.value = 0.5;

        oscillator.start();
        setTimeout(() => {
            oscillator.stop();
            ctx.close();
        }, 200);
    }, [soundEnabled]);

    // Load Model
    useEffect(() => {
        const loadModel = async () => {
            try {
                const tf = await import('@tensorflow/tfjs');
                await import('@tensorflow/tfjs-backend-webgl');
                const faceLandmarksDetection = await import('@tensorflow-models/face-landmarks-detection');

                await tf.setBackend('webgl');
                tf.enableProdMode();
                await tf.ready();
                const loadedModel = await faceLandmarksDetection.createDetector(
                    faceLandmarksDetection.SupportedModels.MediaPipeFaceMesh,
                    {
                        runtime: 'tfjs',
                        refineLandmarks: true,
                        maxFaces: 1,
                    }
                );
                setModel(loadedModel);
                setLoading(false);
            } catch (err) {
                console.error('Failed to load model', err);
                setLoading(false);
            }
        };
        loadModel();
    }, []);

    const euclideanDistance = (p1: { x: number, y: number }, p2: { x: number, y: number }) => {
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    };

    const getEAR = (landmarks: any, indices: number[]) => {
        const p1 = landmarks[indices[0]];
        const p2 = landmarks[indices[1]];
        const p3 = landmarks[indices[2]];
        const p4 = landmarks[indices[3]];
        const p5 = landmarks[indices[4]];
        const p6 = landmarks[indices[5]];

        const v1 = euclideanDistance(p2, p6);
        const v2 = euclideanDistance(p3, p5);
        const h = euclideanDistance(p1, p4);

        return (v1 + v2) / (2.0 * h);
    };

    const closedFrames = useRef(0);

    const detect = async () => {
        if (
            webcamRef.current &&
            webcamRef.current.video &&
            webcamRef.current.video.readyState === 4 &&
            model
        ) {
            const video = webcamRef.current.video;
            const predictions = await model.estimateFaces(video);

            if (predictions.length > 0) {
                const keypoints = predictions[0].keypoints;
                const leftEar = getEAR(keypoints, LEFT_EYE);
                const rightEar = getEAR(keypoints, RIGHT_EYE);

                const avgEar = (leftEar + rightEar) / 2.0;
                setEar(avgEar);

                if (avgEar < EAR_THRESHOLD) {
                    closedFrames.current += 1;
                    if (closedFrames.current >= EAR_FRAMES) {
                        if (!alarm) {
                            setAlarm(true);
                            playAlarm();
                        } else {
                            playAlarm();
                        }
                    }
                } else {
                    closedFrames.current = 0;
                    setAlarm(false);
                }
            }
        }
        if (isProcessing) {
            requestRef.current = requestAnimationFrame(detect);
        }
    };

    useEffect(() => {
        if (isProcessing && model) {
            detect();
        } else {
            if (requestRef.current !== null) {
                cancelAnimationFrame(requestRef.current);
            }
        }
        return () => {
            if (requestRef.current !== null) cancelAnimationFrame(requestRef.current);
        };
    }, [isProcessing, model]);


    useEffect(() => {
        const handleSync = () => setIsOnline(navigator.onLine);
        window.addEventListener('online', handleSync);
        window.addEventListener('offline', handleSync);
        return () => {
            window.removeEventListener('online', handleSync);
            window.removeEventListener('offline', handleSync);
        }
    }, []);

    return (
        <main className={clsx(
            "min-h-screen relative overflow-hidden transition-colors duration-700 flex flex-col items-center justify-center p-6",
            mode === 'day' ? "bg-gradient-to-br from-blue-50 to-indigo-100 text-slate-900" : "bg-gray-900 text-white"
        )}>
            {/* Dynamic Background Blobs */}
            <div className={clsx("absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none opacity-40", mode === 'day' ? 'mix-blend-multiply' : 'mix-blend-screen')}>
                <div className="absolute top-0 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
                <div className="absolute top-0 -right-4 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
                <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
            </div>

            <div className={clsx(
                "relative z-10 max-w-lg w-full rounded-3xl p-6 backdrop-blur-2xl shadow-2xl border transition-all duration-300",
                mode === 'day'
                    ? "bg-white/40 border-white/50"
                    : "bg-black/40 border-white/10"
            )}>
                <header className="flex justify-between items-center mb-6">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-blue-600 rounded-xl shadow-lg">
                            <Eye className="text-white" size={20} />
                        </div>
                        <div>
                            <h1 className="text-xl font-bold tracking-tight">SleepSafe</h1>
                            <div className="flex items-center gap-1.5 mt-0.5">
                                <span className={clsx("w-2 h-2 rounded-full", isOnline ? "bg-emerald-500" : "bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.6)]")} />
                                <span className="text-xs font-medium opacity-60 uppercase tracking-wider">{isOnline ? "Online" : "Offline"}</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex gap-2">
                        <button
                            onClick={() => setSoundEnabled(!soundEnabled)}
                            className={clsx("p-2.5 rounded-xl transition-all duration-200",
                                soundEnabled
                                    ? "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400"
                                    : "bg-rose-500/10 text-rose-600 dark:text-rose-400"
                            )}
                            title={soundEnabled ? "Mute Alarm" : "Unmute Alarm"}
                        >
                            {soundEnabled ? <Volume2 size={20} /> : <VolumeX size={20} />}
                        </button>
                        <button
                            onClick={() => setMode(mode === 'day' ? 'night' : 'day')}
                            className="p-2.5 rounded-xl bg-gray-500/10 hover:bg-gray-500/20 transition-all duration-200"
                        >
                            {mode === 'day' ? <Moon size={20} /> : <Sun size={20} />}
                        </button>
                    </div>
                </header>

                <div className="relative rounded-2xl overflow-hidden shadow-2xl bg-black aspect-[4/3] group">
                    {/* Webcam Feed */}
                    <Webcam
                        ref={webcamRef}
                        audio={false}
                        screenshotFormat="image/jpeg"
                        className={clsx("w-full h-full object-cover transform scale-x-[-1] transition-opacity duration-300", isProcessing ? "opacity-100" : "opacity-40")}
                        videoConstraints={{ facingMode: "user" }}
                    />

                    {/* HUD Overlay */}
                    <div className="absolute top-4 left-4 flex flex-col gap-2">
                        <div className="px-3 py-1.5 rounded-lg bg-black/60 backdrop-blur-md border border-white/10 flex items-center gap-2">
                            <Activity size={14} className={clsx("animate-pulse", avgEar(ear) < EAR_THRESHOLD ? "text-red-400" : "text-emerald-400")} />
                            <span className="text-xs font-mono text-white/90">EAR: {ear.toFixed(2)}</span>
                        </div>
                    </div>

                    {loading && (
                        <div className="absolute inset-0 flex flex-col items-center justify-center bg-black/80 z-20 backdrop-blur-sm">
                            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                            <span className="text-white font-medium animate-pulse">Initializing AI Core...</span>
                        </div>
                    )}

                    {/* Critical Alert Overlay */}
                    <div className={clsx(
                        "absolute inset-0 flex items-center justify-center bg-red-500/60 z-30 transition-all duration-100",
                        alarm ? "opacity-100 scale-100 backdrop-blur-sm" : "opacity-0 scale-95 pointer-events-none"
                    )}>
                        <div className="bg-red-600 text-white px-8 py-6 rounded-2xl font-black text-4xl shadow-2xl border-4 border-white/50 animate-bounce text-center">
                            <AlertCircle className="w-16 h-16 mx-auto mb-2" />
                            WAKE UP!
                        </div>
                    </div>

                    {/* Waiting State */}
                    {!isProcessing && !loading && (
                        <div className="absolute inset-0 flex items-center justify-center">
                            <button
                                onClick={() => setIsProcessing(true)}
                                className="group/btn relative px-8 py-4 bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl overflow-hidden hover:bg-white/20 transition-all duration-300"
                            >
                                <div className="flex flex-col items-center gap-2 text-white group-hover/btn:scale-105 transition-transform">
                                    <Camera size={32} />
                                    <span className="font-semibold">Tap to Start</span>
                                </div>
                            </button>
                        </div>
                    )}
                </div>

                <div className="mt-6 flex flex-col gap-4">
                    {isProcessing && (
                        <button
                            onClick={() => setIsProcessing(false)}
                            className="w-full py-4 rounded-xl font-bold text-white bg-rose-600 hover:bg-rose-700 shadow-lg shadow-rose-600/30 transition-all active:scale-95 flex items-center justify-center gap-2 group"
                        >
                            <div className="w-2 h-2 rounded-full bg-white animate-pulse" />
                            Stop Monitoring
                        </button>
                    )}

                    <div className="grid grid-cols-2 gap-3 text-xs opacity-60 text-center font-medium">
                        <div className="bg-gray-500/5 p-2 rounded-lg border border-gray-500/10">
                            Works Offline
                        </div>
                        <div className="bg-gray-500/5 p-2 rounded-lg border border-gray-500/10">
                            Privacy Focused (Local)
                        </div>
                    </div>
                </div>
            </div>
        </main>
    );
}

// Helper for UI logic
function avgEar(val: number) { return val; } 
