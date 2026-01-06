'use client';

import { motion } from 'framer-motion';
import { FaGithub, FaLinkedin, FaEnvelope, FaCode, FaDatabase, FaMobile, FaServer, FaShieldAlt, FaTools, FaCloud, FaLock, FaNetworkWired, FaGraduationCap } from 'react-icons/fa';
import Navigation from '@/components/Navigation';
import SkillCard from '@/components/SkillCard';
import ProjectCard from '@/components/ProjectCard';
import Hero from '@/components/Hero';

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

export default function Home() {
  const skills = [
    {
      icon: FaShieldAlt,
      title: 'Threat Hunting & SIEM',
      description: 'Expert in ELK Stack, Wazuh, MITRE ATT&CK framework, and real-time security monitoring. Designed SOC-style multi-cloud security environments.',
      level: 'Expert' as const,
    },
    {
      icon: FaLock,
      title: 'Penetration Testing',
      description: 'Certified Ethical Hacker (CEH) with experience in vulnerability assessment, OWASP/NIST frameworks, and reducing attack surfaces by 40%.',
      level: 'Expert' as const,
    },
    {
      icon: FaCloud,
      title: 'Cloud Security',
      description: 'Multi-cloud security expertise (AWS + Azure), automated detection rules, and adversary simulation. Google Cloud DevOps certified.',
      level: 'Advanced' as const,
    },
    {
      icon: FaNetworkWired,
      title: 'Secure Software Engineering',
      description: 'Applied NIST/OWASP standards in banking environments. Expertise in API security, authentication, and secure transaction processing.',
      level: 'Expert' as const,
    },
  ];

  const projects = [
    {
      title: 'Post-Quantum Secure Chat',
      description: 'Web-based messaging prototype demonstrating post-quantum cryptography with Kyber512 key encapsulation and Dilithium2 signatures. Features FastAPI backend, React frontend, and AES-GCM encryption.',
      technologies: ['Python', 'FastAPI', 'React', 'Post-Quantum Crypto', 'Kyber512', 'Dilithium2'],
      // Abstract cryptography + qubits style image
      imageUrl: 'https://images.unsplash.com/photo-1617839625591-e5a789593135?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
      githubUrl: 'https://github.com/Marouane7709/post-quantum-secure-chat',
    },
    {
      title: 'Cloud Security & Threat Hunting Lab',
      description: 'Designed a SOC-style multi-cloud security monitoring environment (AWS + Azure) using ELK Stack and Wazuh. Developed MITRE ATT&CK-aligned detection rules and automated real-time security alerts.',
      technologies: ['AWS', 'Azure', 'ELK Stack', 'Wazuh', 'MITRE ATT&CK', 'SIEM'],
      // Cloud + security visual
      imageUrl: 'https://plus.unsplash.com/premium_photo-1683836722608-60ab4d1b58e5?q=80&w=1112&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    },
    {
      title: 'Ethical Hacking & Penetration Testing',
      description: 'Performed structured vulnerability assessments and penetration testing on enterprise systems. Identified 35+ vulnerabilities mapped to OWASP and NIST frameworks, reducing attack surface by 40%.',
      technologies: ['Penetration Testing', 'OWASP', 'NIST', 'Vulnerability Assessment', 'CEH'],
      imageUrl: 'https://images.unsplash.com/photo-1510915228340-29c85a43dcfe?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    },
    {
      title: 'TryHackMe Security Labs',
      description: 'Completed numerous hands-on cybersecurity labs covering penetration testing, network security, web application security, and cryptography. Practical experience with real-world attack scenarios and defense mechanisms.',
      technologies: ['TryHackMe', 'Penetration Testing', 'Network Security', 'Web Security', 'Cryptography'],
      imageUrl: 'https://s3-eu-west-1.amazonaws.com/tpd/logos/5f00b0f031ec4d0001f1344e/0x0.png',
    },
    {
      title: 'Secure Banking API Optimization',
      description: 'Optimized secure banking transactions at Crédit du Maroc by improving fund authorization, balance updates, and API performance. Applied NIST/OWASP standards for secure API validation and access controls.',
      technologies: ['Java', 'Spring Boot', 'API Security', 'NIST', 'OWASP', 'Banking Systems'],
      imageUrl: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=600&fit=crop&q=80',
    },
    {
      title: 'AI Checkers Game',
      description: 'Developed an intelligent checkers game featuring multiple AI algorithms (Minimax, Alpha-Beta Pruning) with performance analytics and an interactive GUI using Python and Turtle graphics.',
      technologies: ['Python', 'AI Algorithms', 'Turtle Graphics', 'Game Development'],
      imageUrl: '/images/checkers.jpg',
    },
    {
      title: 'CubeSat Budget Analyzer',
      description: 'Professional-grade desktop application for analyzing CubeSat mission budgets, featuring comprehensive link and data budget analysis with an intuitive Qt-based GUI.',
      technologies: ['Python', 'PyQt6', 'Satellite Communications', 'Data Analysis'],
      // CubeSat / small satellite style image
      imageUrl: 'https://images.unsplash.com/photo-1708738793054-32b71e3fc822?q=80&w=1440&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
    },
    {
      title: 'E-commerce Platform Testing',
      description: 'Developed and implemented automated test scripts using Selenium to evaluate functionality, performance, and security.',
      technologies: ['Selenium', 'Java', 'Automated Testing'],
      imageUrl: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&q=80',
    },
    {
      title: 'Delivery App',
      description: 'Developed a mobile app for food ordering using modern web technologies with a focus on user experience.',
      technologies: ['JavaScript', 'Node.js', 'React'],
      imageUrl: 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800&h=600&fit=crop&q=80',
    },
  ];

  return (
    <div className="relative">
      <Hero />
      <main className="min-h-screen">
        {/* Skills Section */}
        <section id="skills" className="section-container relative overflow-hidden">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 w-screen h-full bg-gray-900/50 -z-10" />
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-12"
          >
            <motion.h2 
              className="heading-2 text-center mb-16 gradient-text"
              variants={fadeInUp}
            >
              Skills & Expertise
            </motion.h2>
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8"
              variants={fadeInUp}
            >
              {skills.map((skill, index) => (
                <SkillCard key={index} {...skill} />
              ))}
            </motion.div>
          </motion.div>
        </section>

        {/* Education Section */}
        <section id="education" className="section-container relative overflow-hidden">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 w-screen h-full bg-gray-900/50 -z-10" />
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-12"
          >
            <motion.h2 
              className="heading-2 text-center mb-16 gradient-text"
              variants={fadeInUp}
            >
              Education
            </motion.h2>
            <motion.div 
              className="max-w-4xl mx-auto space-y-8"
              variants={fadeInUp}
            >
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5 }}
                className="bg-gray-800/95 backdrop-blur-lg rounded-xl p-8 border border-gray-700/50 shadow-xl"
              >
                <div className="flex items-start gap-6">
                  <div className="p-4 rounded-lg bg-green-900/50">
                    <FaGraduationCap className="text-3xl text-green-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-white mb-2">Master of Science in Cybersecurity</h3>
                    <p className="text-green-400 font-medium mb-2">University of Wollongong, Dubai, UAE</p>
                    <p className="text-gray-300">Currently pursuing a Master's degree in Cybersecurity, specializing in threat hunting, penetration testing, and post-quantum cryptography.</p>
                  </div>
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="bg-gray-800/95 backdrop-blur-lg rounded-xl p-8 border border-gray-700/50 shadow-xl"
              >
                <div className="flex items-start gap-6">
                  <div className="p-4 rounded-lg bg-green-900/50">
                    <FaGraduationCap className="text-3xl text-green-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-2xl font-bold text-white mb-2">Bachelor of Science in Computer Science</h3>
                    <p className="text-green-400 font-medium mb-2">Al Akhawayn University, Ifrane, Morocco</p>
                    <p className="text-gray-300 mb-3">Completed Bachelor's degree in Computer Science with a strong foundation in software engineering, algorithms, and system design.</p>
                    <div className="mt-4 pt-4 border-t border-gray-700/50">
                      <p className="text-sm text-gray-400">
                        <span className="text-green-400 font-medium">Exchange Semester:</span> Monroe University, New York, USA
                      </p>
                    </div>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </motion.div>
        </section>

        {/* Projects Section */}
        <section id="projects" className="section-container relative overflow-hidden">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 w-screen h-full bg-gradient-to-br from-gray-900/50 to-gray-800/50 -z-10" />
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="space-y-12"
          >
            <motion.h2 
              className="heading-2 text-center mb-16 gradient-text"
              variants={fadeInUp}
            >
              My Projects
            </motion.h2>
            <motion.div 
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
              variants={fadeInUp}
            >
              {projects.map((project, index) => (
                <ProjectCard key={index} {...project} />
              ))}
            </motion.div>
          </motion.div>
        </section>

        {/* Contact Section */}
        <section id="contact" className="section-container relative overflow-hidden">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 w-screen h-full bg-gray-900/50 -z-10" />
          <motion.div
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
            className="text-center space-y-12"
          >
            <motion.h2 
              className="heading-2 gradient-text mb-16"
              variants={fadeInUp}
            >
              Get in Touch
            </motion.h2>
            <motion.div 
              className="flex justify-center gap-8"
              variants={fadeInUp}
            >
              <a
                href="https://github.com/Marouane7709/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-3xl text-gray-300 hover:text-green-400 transition-all duration-300 hover:scale-110"
              >
                <FaGithub />
              </a>
              <a
                href="https://linkedin.com/in/marouane-es-said-31765a270"
                target="_blank"
                rel="noopener noreferrer"
                className="text-3xl text-gray-300 hover:text-green-400 transition-all duration-300 hover:scale-110"
              >
                <FaLinkedin />
              </a>
              <a
                href="mailto:Marouaneessaid09@gmail.com"
                className="text-3xl text-gray-300 hover:text-green-400 transition-all duration-300 hover:scale-110"
              >
                <FaEnvelope />
              </a>
            </motion.div>
          </motion.div>
        </section>
      </main>
    </div>
  );
} 