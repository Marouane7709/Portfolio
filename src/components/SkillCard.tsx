import { motion } from 'framer-motion';
import { IconType } from 'react-icons';

interface SkillCardProps {
  icon: IconType;
  title: string;
  description: string;
  level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
}

const SkillCard = ({ icon: Icon, title, description, level }: SkillCardProps) => {
  const getLevelColor = (level: string) => {
    switch (level) {
      case 'Beginner':
        return 'bg-blue-900/80 text-blue-200';
      case 'Intermediate':
        return 'bg-green-900/80 text-green-200';
      case 'Advanced':
        return 'bg-yellow-900/80 text-yellow-200';
      case 'Expert':
        return 'bg-purple-900/80 text-purple-200';
      default:
        return 'bg-gray-900/80 text-gray-200';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      whileHover={{ y: -5 }}
      className="glass-card p-6 group bg-gray-800/95 border-gray-700/30"
    >
      <div className="flex items-center mb-4">
        <div className="p-3 rounded-lg bg-blue-900/50 group-hover:bg-blue-800/50 transition-colors">
          <Icon className="text-3xl text-blue-400" />
        </div>
        <h3 className="text-xl font-semibold ml-4 gradient-text">{title}</h3>
      </div>
      <p className="text-gray-300 mb-4 leading-relaxed">{description}</p>
      <span className={`inline-block px-4 py-1.5 rounded-full text-sm font-medium backdrop-blur-sm ${getLevelColor(level)}`}>
        {level}
      </span>
    </motion.div>
  );
};

export default SkillCard; 