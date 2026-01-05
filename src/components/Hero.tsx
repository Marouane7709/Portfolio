'use client';

import { motion } from 'framer-motion';
import { HiArrowDown, HiShieldCheck, HiLockClosed, HiGlobeAlt, HiDatabase } from 'react-icons/hi';
import { FaShieldAlt, FaNetworkWired, FaBug } from 'react-icons/fa';

const Hero = () => {
  const handleScrollToProjects = () => {
    document.getElementById('projects')?.scrollIntoView({ behavior: 'smooth' });
  };

  const achievements = [
    { value: '35+', label: 'Vulnerabilities Identified', icon: FaBug },
    { value: '40%', label: 'Attack Surface Reduction', icon: HiShieldCheck },
    { value: '100%', label: 'Test Coverage', icon: HiLockClosed },
  ];

  const services = [
    { name: 'Threat Hunting', icon: FaShieldAlt },
    { name: 'Network Security', icon: FaNetworkWired },
    { name: 'Web Security', icon: HiGlobeAlt },
    { name: 'Database Security', icon: HiDatabase },
  ];

  return (
    <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 pt-24">
      {/* Subtle grid pattern background */}
      <div className="absolute inset-0 opacity-[0.03]">
        <div className="absolute inset-0" style={{
          backgroundImage: `linear-gradient(rgba(34, 197, 94, 0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(34, 197, 94, 0.08) 1px, transparent 1px)`,
          backgroundSize: '50px 50px'
        }} />
      </div>

      {/* Subtle radial gradient */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(34,197,94,0.08),transparent_60%)]" />

      <div className="container mx-auto px-6 sm:px-8 lg:px-12 relative z-10 py-16 sm:py-20 lg:py-24">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Side - Main Content */}
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="text-white space-y-6"
          >
            <motion.p
              className="text-sm md:text-base text-green-400 font-medium tracking-wider uppercase"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
            >
              Hello I'm
            </motion.p>
            
            <motion.h1
              className="text-5xl md:text-6xl lg:text-7xl font-bold text-green-400 leading-tight tracking-tight"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              Marouane<br />ES-SAID
            </motion.h1>

            <motion.p
              className="text-xl md:text-2xl text-white/95 font-medium"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
            >
              Cyber Security Expert
            </motion.p>

            <motion.p
              className="text-base md:text-lg text-gray-300 leading-relaxed max-w-lg"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
            >
              MSc Cybersecurity student at University of Wollongong Dubai, specializing in threat hunting, penetration testing, and post-quantum cryptography. Experienced in secure software engineering, SIEM operations, and vulnerability assessment with proven results in enterprise security.
            </motion.p>

            <motion.button
              onClick={handleScrollToProjects}
              className="bg-green-500 hover:bg-green-600 text-slate-900 font-semibold px-8 py-3.5 rounded-lg transition-all duration-300 shadow-lg shadow-green-500/30 hover:shadow-green-500/50 mt-4"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Get Started
            </motion.button>
          </motion.div>

          {/* Right Side - Cards */}
          <div className="space-y-5">
            {/* Achievements Card */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="bg-slate-800/70 backdrop-blur-md rounded-xl p-6 border border-slate-700/50 shadow-xl"
            >
              <h3 className="text-lg font-bold text-green-400 text-center mb-6 tracking-wide">MY ACHIEVEMENTS</h3>
              <div className="grid grid-cols-3 gap-6">
                {achievements.map((achievement, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.4, delay: 0.3 + index * 0.1 }}
                    className="text-center space-y-2"
                  >
                    <achievement.icon className="text-2xl text-green-400 mx-auto" />
                    <div className="text-2xl font-bold text-white">{achievement.value}</div>
                    <div className="text-xs text-gray-400 leading-tight">{achievement.label}</div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            {/* Services Card */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="bg-slate-800/70 backdrop-blur-md rounded-xl p-6 border border-slate-700/50 shadow-xl"
            >
              <h3 className="text-lg font-bold text-green-400 text-center mb-6 tracking-wide">WHICH SERVICE I PROVIDE AND LEARN</h3>
              <div className="grid grid-cols-2 gap-3 mb-5">
                {services.map((service, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 0.4, delay: 0.4 + index * 0.1 }}
                    className="flex flex-col items-center p-4 rounded-lg bg-slate-700/30 hover:bg-slate-700/50 transition-colors cursor-pointer border border-slate-600/30"
                  >
                    <service.icon className="text-2xl text-green-400 mb-2" />
                    <span className="text-sm text-white font-medium">{service.name}</span>
                  </motion.div>
                ))}
              </div>
              <div className="grid grid-cols-2 gap-4 pt-5 border-t border-slate-700/50">
                <div className="text-center">
                  <div className="text-xl font-bold text-green-400">35+</div>
                  <div className="text-xs text-gray-400 mt-1">Vulnerabilities Found</div>
                </div>
                <div className="text-center">
                  <div className="text-xl font-bold text-green-400">40%</div>
                  <div className="text-xs text-gray-400 mt-1">Attack Reduction</div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <motion.div
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.6, delay: 0.8 }}
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
        >
          <HiArrowDown className="text-3xl text-green-400/70" />
        </motion.div>
      </motion.div>
    </section>
  );
};

export default Hero;
