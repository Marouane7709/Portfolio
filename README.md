# Modern Portfolio Website

A modern, responsive portfolio website built with Next.js, TypeScript, and Tailwind CSS. This portfolio is designed to showcase your skills, projects, and professional experience in a way that attracts recruiters and potential employers.

## Features

- 🎨 Modern and clean design
- 📱 Fully responsive layout
- 🌓 Dark/Light mode support
- ⚡ Fast performance with Next.js
- 🎯 SEO optimized
- ✨ Smooth animations with Framer Motion
- 🎨 Customizable color scheme
- 📝 Easy to update content

## Getting Started

1. Clone the repository:
   ```bash
   git clone [your-repo-url]
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Customization

### Personal Information

1. Update your name and title in `src/app/page.tsx`
2. Add your social media links in the contact section
3. Update the hero section with your value proposition

### Skills

Edit the `skills` array in `src/app/page.tsx` to showcase your expertise:

```typescript
const skills = [
  {
    icon: FaCode,
    title: 'Your Skill',
    description: 'Description of your expertise',
    level: 'Expert' as const,
  },
  // Add more skills...
];
```

### Projects

Update the `projects` array in `src/app/page.tsx` with your work:

```typescript
const projects = [
  {
    title: 'Project Name',
    description: 'Project description',
    technologies: ['Tech1', 'Tech2'],
    imageUrl: '/images/project1.jpg',
    githubUrl: 'Your GitHub URL',
    liveUrl: 'Live Demo URL',
  },
  // Add more projects...
];
```

### Images

1. Add your project images to the `public/images` directory
2. Update the `imageUrl` in the projects array to match your image paths

### Styling

The portfolio uses Tailwind CSS for styling. You can customize:

1. Colors in `tailwind.config.js`
2. Typography in `src/app/globals.css`
3. Layout in the component files

## Deployment

The portfolio can be easily deployed to Vercel:

1. Push your code to GitHub
2. Import your repository in Vercel
3. Deploy with default settings

## Best Practices for Recruiters

This portfolio is designed with recruiters in mind:

1. **Clear Value Proposition**: The hero section immediately communicates your unique value
2. **Skills Showcase**: Skills are presented with clear proficiency levels
3. **Project Highlights**: Projects demonstrate real-world experience and technical abilities
4. **Easy Contact**: Multiple ways for recruiters to reach out
5. **Professional Design**: Clean, modern design that reflects attention to detail

## Contributing

Feel free to fork this repository and customize it for your needs. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is open source and available under the [MIT License](LICENSE). 